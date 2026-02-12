#!/usr/bin/env python3
"""
Production-ready web frontend for Travel PDF to ICS Converter
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from travel_to_ics import TravelPDFParser
from custom_ics_generator import CustomICSGenerator
from google_calendar_integration import GoogleCalendarIntegration
from pathlib import Path
import tempfile
import secrets

app = Flask(__name__)
# Production secret key - change this!
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page with upload form."""
    return render_template('index_with_google.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and conversion."""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a PDF file.', 'error')
        return redirect(url_for('index'))

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)

        # Parse PDF
        parser = TravelPDFParser(pdf_path)
        flights = parser.parse_flights()
        hotels = parser.parse_hotels()

        if not flights and not hotels:
            flash('No flights or hotels found in the PDF. Please check if the PDF format is compatible.', 'warning')
            os.remove(pdf_path)
            return redirect(url_for('index'))

        # Get custom settings from form
        flight_color = request.form.get('flight_color', '11')
        hotel_color = request.form.get('hotel_color', '6')
        output_method = request.form.get('output_method', 'ics')

        # Get airport commute times
        airport_times = {}
        for key in ['scl_before', 'scl_after', 'aep_before', 'aep_after',
                   'eze_before', 'eze_after', 'gru_before', 'gru_after',
                   'mex_before', 'mex_after', 'international_before', 'international_after']:
            if key in request.form:
                # Convert to uppercase for airport code
                parts = key.split('_')
                airport_code = parts[0].upper()
                direction = parts[1]
                airport_times[f'{airport_code}_{direction}'] = request.form[key]

        # Store data in session for Google Calendar flow (serialize datetime objects)
        flights_serialized = []
        for f in flights:
            f_dict = {
                'flight_number': f.flight_number,
                'origin': f.origin,
                'destination': f.destination,
                'departure_time': f.departure_time.isoformat(),
                'arrival_time': f.arrival_time.isoformat(),
                'reservation_code': f.reservation_code,
                'ticket_number': f.ticket_number
            }
            flights_serialized.append(f_dict)

        hotels_serialized = []
        for h in hotels:
            h_dict = {
                'name': h.name,
                'checkin_date': h.checkin_date.isoformat(),
                'checkout_date': h.checkout_date.isoformat(),
                'confirmation_number': h.confirmation_number,
                'address': h.address,
                'phone': h.phone,
                'details': h.details,
                'timezone': h.timezone
            }
            hotels_serialized.append(h_dict)

        session['flights'] = flights_serialized
        session['hotels'] = hotels_serialized
        session['flight_color'] = flight_color
        session['hotel_color'] = hotel_color
        session['airport_times'] = airport_times

        # Clean up PDF
        os.remove(pdf_path)

        if output_method == 'google':
            # Redirect to Google OAuth
            return redirect(url_for('google_auth'))
        else:
            # Generate ICS file
            generator = CustomICSGenerator(
                flight_color=flight_color,
                hotel_color=hotel_color,
                airport_times=airport_times
            )
            generator.process_flights(flights)

            for hotel in hotels:
                generator.add_hotel_event(hotel)

            # Save ICS file
            ics_filename = Path(filename).stem + '.ics'
            ics_path = os.path.join(app.config['UPLOAD_FOLDER'], ics_filename)
            generator.save(ics_path)

            # Show success message
            flash(f'Successfully converted! Found {len(flights)} flights and {len(hotels)} hotels.', 'success')

            # Send file
            return send_file(
                ics_path,
                as_attachment=True,
                download_name=ics_filename,
                mimetype='text/calendar'
            )

    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        # Clean up files on error
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return redirect(url_for('index'))


@app.route('/about')
def about():
    """About page with instructions."""
    return render_template('about.html')


@app.route('/google-auth')
def google_auth():
    """Initiate Google OAuth flow."""
    try:
        gcal = GoogleCalendarIntegration()
        redirect_uri = url_for('google_callback', _external=True)
        authorization_url, state = gcal.get_authorization_url(redirect_uri)

        # Store state in session for verification
        session['oauth_state'] = state

        return redirect(authorization_url)
    except Exception as e:
        flash(f'Error initiating Google authentication: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/google-callback')
def google_callback():
    """Handle Google OAuth callback."""
    try:
        # Verify state
        state = session.get('oauth_state')
        if not state:
            flash('Invalid authentication state', 'error')
            return redirect(url_for('index'))

        # Get full callback URL
        authorization_response = request.url
        redirect_uri = url_for('google_callback', _external=True)

        # Exchange code for credentials
        gcal = GoogleCalendarIntegration()
        gcal.handle_oauth_callback(authorization_response, state, redirect_uri)

        # Retrieve stored data from session
        from travel_to_ics import FlightInfo, HotelInfo
        from datetime import datetime

        flights_data = session.get('flights', [])
        hotels_data = session.get('hotels', [])
        flight_color = session.get('flight_color', '11')
        hotel_color = session.get('hotel_color', '6')
        airport_times = session.get('airport_times', {})

        # Reconstruct objects
        flights = []
        for f_data in flights_data:
            flight = FlightInfo()
            flight.flight_number = f_data['flight_number']
            flight.origin = f_data['origin']
            flight.destination = f_data['destination']
            flight.departure_time = datetime.fromisoformat(f_data['departure_time'])
            flight.arrival_time = datetime.fromisoformat(f_data['arrival_time'])
            flight.reservation_code = f_data['reservation_code']
            flight.ticket_number = f_data.get('ticket_number')
            flights.append(flight)

        hotels = []
        for h_data in hotels_data:
            hotel = HotelInfo()
            hotel.name = h_data['name']
            hotel.checkin_date = datetime.fromisoformat(h_data['checkin_date'])
            hotel.checkout_date = datetime.fromisoformat(h_data['checkout_date'])
            hotel.confirmation_number = h_data.get('confirmation_number')
            hotel.address = h_data.get('address')
            hotel.phone = h_data.get('phone')
            hotel.details = h_data.get('details')
            hotel.timezone = h_data.get('timezone', 'UTC')
            hotels.append(hotel)

        # Create events in Google Calendar
        events_created = 0

        # Create flight events with commutes
        generator = CustomICSGenerator(
            flight_color=flight_color,
            hotel_color=hotel_color,
            airport_times=airport_times
        )

        # Process flights to get commute info
        processed_flights = generator._prepare_flights_with_commutes(flights)

        for flight_data in processed_flights:
            flight = flight_data['flight']

            # Create commute before (if needed)
            if flight_data.get('commute_before'):
                commute = flight_data['commute_before']
                gcal.create_commute_event(
                    title=commute['title'],
                    start_datetime=commute['start'],
                    end_datetime=commute['end'],
                    timezone=commute['timezone'],
                    description=commute.get('description', ''),
                    color_id=flight_color
                )
                events_created += 1

            # Create flight event
            gcal.create_flight_event(flight, color_id=flight_color)
            events_created += 1

            # Create commute after (if needed)
            if flight_data.get('commute_after'):
                commute = flight_data['commute_after']
                gcal.create_commute_event(
                    title=commute['title'],
                    start_datetime=commute['start'],
                    end_datetime=commute['end'],
                    timezone=commute['timezone'],
                    description=commute.get('description', ''),
                    color_id=flight_color
                )
                events_created += 1

        # Create hotel events
        for hotel in hotels:
            gcal.create_hotel_event(hotel, color_id=hotel_color)
            events_created += 1

        # Clear session data
        session.pop('flights', None)
        session.pop('hotels', None)
        session.pop('flight_color', None)
        session.pop('hotel_color', None)
        session.pop('airport_times', None)
        session.pop('oauth_state', None)

        flash(f'✅ Successfully created {events_created} events in your Google Calendar!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        flash(f'Error creating Google Calendar events: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring."""
    return {'status': 'healthy', 'service': 'travel-to-ics'}, 200


if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    print("="*60)
    print("  ✈️  Travel to ICS Converter - Production Mode")
    print("="*60)
    print(f"\n🌐 Running on port: {port}")
    print(f"🔒 Debug mode: {debug}")
    print(f"🔑 Secret key: {'Set' if app.secret_key else 'Not set (using default)'}")
    print("\n⚠️  For production, use a WSGI server like Gunicorn:")
    print(f"   gunicorn -w 4 -b 0.0.0.0:{port} web_app_production:app")
    print("="*60 + "\n")

    app.run(debug=debug, host='0.0.0.0', port=port)

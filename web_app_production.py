#!/usr/bin/env python3
"""
Simple web frontend for Travel PDF to ICS Converter
ICS download only with customizable colors and commute times
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from travel_to_ics import TravelPDFParser
from custom_ics_generator import CustomICSGenerator
from pathlib import Path
import tempfile
import secrets
import pickle
import uuid

app = Flask(__name__)
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
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and show preview."""
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

        # Clean up PDF
        os.remove(pdf_path)

        # Generate unique session ID
        session_id = str(uuid.uuid4())

        # Store parsed data in session (serialize objects)
        session[f'flights_{session_id}'] = pickle.dumps(flights)
        session[f'hotels_{session_id}'] = pickle.dumps(hotels)
        session[f'filename_{session_id}'] = filename

        # Redirect to preview page
        return redirect(url_for('preview', session_id=session_id))

    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        # Clean up files on error
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return redirect(url_for('index'))


@app.route('/preview/<session_id>')
def preview(session_id):
    """Show preview of parsed data."""
    try:
        # Retrieve data from session
        flights_data = session.get(f'flights_{session_id}')
        hotels_data = session.get(f'hotels_{session_id}')

        if not flights_data and not hotels_data:
            flash('Session expired. Please upload your PDF again.', 'warning')
            return redirect(url_for('index'))

        flights = pickle.loads(flights_data) if flights_data else []
        hotels = pickle.loads(hotels_data) if hotels_data else []

        return render_template('preview.html',
                             flights=flights,
                             hotels=hotels,
                             session_id=session_id)
    except Exception as e:
        flash(f'Error loading preview: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/generate', methods=['POST'])
def generate_ics():
    """Generate ICS file from session data and custom settings."""
    session_id = request.form.get('session_id')

    if not session_id:
        flash('Invalid session', 'error')
        return redirect(url_for('index'))

    try:
        # Retrieve data from session
        flights_data = session.get(f'flights_{session_id}')
        hotels_data = session.get(f'hotels_{session_id}')
        filename = session.get(f'filename_{session_id}', 'travel.pdf')

        if not flights_data and not hotels_data:
            flash('Session expired. Please upload your PDF again.', 'warning')
            return redirect(url_for('index'))

        flights = pickle.loads(flights_data) if flights_data else []
        hotels = pickle.loads(hotels_data) if hotels_data else []

        # Get custom settings from form
        flight_color = request.form.get('flight_color', '11')
        hotel_color = request.form.get('hotel_color', '6')

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

        # Generate ICS with custom settings
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

        # Clean up session data
        session.pop(f'flights_{session_id}', None)
        session.pop(f'hotels_{session_id}', None)
        session.pop(f'filename_{session_id}', None)

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
        flash(f'Error generating ICS file: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/about')
def about():
    """About page with instructions."""
    return render_template('about.html')


@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring."""
    return {
        'status': 'healthy',
        'service': 'travel-to-ics',
        'features': {
            'ics_download': True,
            'customization': True
        }
    }, 200


if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    print("="*60)
    print("  ✈️  Travel to ICS Converter - Simple Mode")
    print("="*60)
    print(f"\n🌐 Running on port: {port}")
    print(f"🔒 Debug mode: {debug}")
    print("\n⚠️  For production, use a WSGI server like Gunicorn:")
    print(f"   gunicorn -w 4 -b 0.0.0.0:{port} web_app_simple:app")
    print("="*60 + "\n")

    app.run(debug=debug, host='0.0.0.0', port=port)

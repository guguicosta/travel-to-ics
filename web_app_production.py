#!/usr/bin/env python3
"""
Production-ready web frontend for Travel PDF to ICS Converter
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from travel_to_ics import TravelPDFParser, ICSGenerator
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
    return render_template('index.html')


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

        # Generate ICS
        generator = ICSGenerator()
        generator.process_flights(flights)

        for hotel in hotels:
            generator.add_hotel_event(hotel)

        # Save ICS file
        ics_filename = Path(filename).stem + '.ics'
        ics_path = os.path.join(app.config['UPLOAD_FOLDER'], ics_filename)
        generator.save(ics_path)

        # Clean up PDF
        os.remove(pdf_path)

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

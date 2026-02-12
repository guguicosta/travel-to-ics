#!/usr/bin/env python3
"""
Web frontend for Travel PDF to ICS Converter
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from travel_to_ics import TravelPDFParser, ICSGenerator
from pathlib import Path
import tempfile

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

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


if __name__ == '__main__':
    # Create templates folder if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    # Try port 5000 first, fallback to 8080 if unavailable
    import socket

    def is_port_available(port):
        """Check if a port is available"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('0.0.0.0', port))
            sock.close()
            return True
        except OSError:
            return False

    # Determine which port to use
    if is_port_available(5000):
        port = 5000
    elif is_port_available(8080):
        port = 8080
        print("\n⚠️  Port 5000 is in use (possibly AirPlay Receiver)")
        print("   Using port 8080 instead")
    else:
        port = 8888
        print("\n⚠️  Ports 5000 and 8080 are in use")
        print("   Using port 8888 instead")

    print("\n" + "="*60)
    print("  ✈️  Travel to ICS Converter Web App")
    print("="*60)
    print(f"\n🌐 Open your browser to:")
    print(f"   http://localhost:{port}")
    print(f"   http://127.0.0.1:{port}")
    print(f"\n📱 Or from another device on your network:")
    print(f"   http://192.168.86.30:{port}")
    print(f"\n⌨️  Press CTRL+C to stop the server")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=port)

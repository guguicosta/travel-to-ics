# 🌐 Web App Guide

## Quick Start

### Option 1: Using the Startup Script (Easiest)

```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
./start_web_app.sh
```

### Option 2: Direct Python Command

```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
python3 web_app.py
```

Then open your browser to: **http://localhost:5000**

## How to Use

1. **Open the App** - Navigate to http://localhost:5000 in your web browser

2. **Upload PDF** - Either:
   - Click the upload area and select your CWT PDF file
   - Drag and drop your PDF file onto the upload area

3. **Convert** - Click the "Convert to Calendar" button

4. **Download** - The ICS file will automatically download to your computer

5. **Import to Google Calendar**:
   - Open Google Calendar (https://calendar.google.com)
   - Click Settings ⚙️ → Import & Export
   - Choose the downloaded .ics file
   - Select your destination calendar
   - Click Import

## Features

### Beautiful Interface
- Modern, responsive design
- Drag & drop file upload
- Real-time processing feedback
- Mobile-friendly

### Easy to Use
- No command line knowledge needed
- Visual upload progress
- Clear success/error messages
- Automatic file download

### Safe & Private
- Files processed locally on your computer
- PDFs are immediately deleted after conversion
- No data sent to external servers
- No file storage

## Troubleshooting

### Port Already in Use

If you see "Address already in use", another app is using port 5000. You can either:

1. **Stop the other app**, or
2. **Change the port** by editing `web_app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=8080)  # Change to 8080 or any other port
   ```

### Can't Access from Another Device

To access the app from another device on your network:

1. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. Access the app from another device using:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

### File Upload Fails

- Check that the file is a valid PDF (under 16MB)
- Ensure the PDF is from CWT travel agents
- Try closing and reopening the browser

### "Module Not Found" Error

Install the required dependencies:
```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
pip3 install -r requirements.txt
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Production Deployment

**⚠️ Important:** This web app is designed for local use. If you want to deploy it to a production server:

1. Change the secret key in `web_app.py`:
   ```python
   app.secret_key = 'your-strong-random-secret-key-here'
   ```

2. Set `debug=False` in the run command:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

3. Use a production WSGI server like Gunicorn:
   ```bash
   pip3 install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
   ```

4. Consider using HTTPS and proper authentication

## File Structure

```
/Users/agcosta/Proyecto Claude EA viajes/
├── web_app.py              # Flask web application
├── start_web_app.sh        # Startup script
├── travel_to_ics.py        # Core conversion logic
├── templates/
│   ├── base.html          # Base template with styling
│   ├── index.html         # Upload page
│   └── about.html         # Information page
└── requirements.txt        # Python dependencies
```

## Browser Compatibility

Tested and works with:
- ✅ Chrome / Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## Tips

- **Bookmark the URL**: Add http://localhost:5000 to your bookmarks for quick access
- **Multiple Files**: You can convert multiple PDFs one after another without restarting
- **Keep Terminal Open**: The terminal window must stay open while using the app
- **Batch Processing**: For multiple files, just upload them one at a time

## Support

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify your PDF is from CWT and in the correct format
3. Ensure all dependencies are installed
4. Try restarting the server

Enjoy converting your travel itineraries! ✈️🏨📅

#!/bin/bash

# Travel to ICS Web App Startup Script

echo "🚀 Starting Travel to ICS Converter Web App..."
echo ""
echo "📍 The app will be available at:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 web_app.py

#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🔍 Travel to ICS - Debug Startup Script                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Change to script directory
cd "$(dirname "$0")"

echo "📍 Working directory: $(pwd)"
echo ""

# Check Python
echo "🐍 Checking Python..."
if command -v python3 &> /dev/null; then
    echo "   ✓ Python 3 found: $(python3 --version)"
else
    echo "   ✗ Python 3 not found!"
    exit 1
fi
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
python3 << 'EOFPYTHON'
import sys
modules = [('flask', 'Flask'), ('icalendar', 'icalendar'), ('PyPDF2', 'PyPDF2')]
all_ok = True
for import_name, display_name in modules:
    try:
        __import__(import_name)
        print(f"   ✓ {display_name}")
    except ImportError:
        print(f"   ✗ {display_name} - NOT INSTALLED")
        all_ok = False

if not all_ok:
    print("\n❌ Missing dependencies! Run:")
    print("   pip3 install -r requirements.txt")
    sys.exit(1)
EOFPYTHON

if [ $? -ne 0 ]; then
    exit 1
fi
echo ""

# Check files
echo "📄 Checking files..."
for file in "web_app.py" "travel_to_ics.py" "templates/index.html" "templates/about.html" "templates/base.html"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file - MISSING!"
    fi
done
echo ""

# Check ports
echo "🔌 Checking ports..."
python3 << 'EOFPYTHON'
import socket

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        sock.close()
        return True
    except OSError:
        return False

for port in [5000, 8080, 8888]:
    if check_port(port):
        print(f"   ✓ Port {port} is available")
    else:
        print(f"   ⚠️  Port {port} is in use")
EOFPYTHON
echo ""

# Get IP addresses
echo "🌐 Your IP addresses:"
if command -v ifconfig &> /dev/null; then
    ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print "   - " $2}' | head -3
fi
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                 🚀 Starting Web Server...                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "⌨️  Press CTRL+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the app
python3 web_app.py

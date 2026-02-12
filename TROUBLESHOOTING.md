# 🔧 Troubleshooting Guide

## Can't Access the Web App in Browser

### Quick Fix Checklist

1. **Is the server running?**
   ```bash
   cd "/Users/agcosta/Proyecto Claude EA viajes"
   ./start_web_app.sh
   ```
   You should see:
   ```
   ============================================================
     ✈️  Travel to ICS Converter Web App
   ============================================================

   🌐 Open your browser to:
      http://localhost:5000
   ```

2. **Try all these URLs:**
   - http://localhost:5000
   - http://127.0.0.1:5000
   - http://0.0.0.0:5000
   - http://localhost:8080 (if 5000 doesn't work)

3. **Double-click this file to auto-open:**
   - `OPEN_APP.html` (will try multiple ports automatically)

---

## Common Issues & Solutions

### Issue 1: "This site can't be reached" or "Connection refused"

**Cause:** Server isn't running

**Solution:**
```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
./start_web_app.sh
```

Keep the terminal window open while using the app!

---

### Issue 2: "Port 5000 already in use" (macOS)

**Cause:** AirPlay Receiver uses port 5000

**Solution:**
1. Open **System Settings**
2. Go to **General** → **AirDrop & Handoff**
3. Turn **OFF** "AirPlay Receiver"
4. Restart the web app

**Alternative:** The app will automatically use port 8080 if 5000 is busy:
- Try http://localhost:8080

---

### Issue 3: Browser shows "Waiting..." or spins forever

**Cause:** Firewall or browser cache

**Solutions:**

1. **Hard refresh the page:**
   - Chrome/Firefox: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
   - Safari: `Cmd+Option+R`

2. **Clear browser cache:**
   - Chrome: Settings → Privacy → Clear browsing data
   - Firefox: Settings → Privacy → Clear Data
   - Safari: Safari menu → Clear History

3. **Try a different browser:**
   - Chrome
   - Firefox
   - Safari
   - Edge

4. **Check firewall:**
   ```bash
   # Temporarily disable firewall (macOS)
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off

   # Re-enable after testing
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
   ```

---

### Issue 4: "Module not found" error in terminal

**Cause:** Dependencies not installed

**Solution:**
```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
pip3 install -r requirements.txt
```

---

### Issue 5: Terminal shows errors when starting

**Check 1 - Flask installed?**
```bash
python3 -c "import flask; print('Flask OK')"
```

**Check 2 - Templates exist?**
```bash
ls -la templates/
# Should show: base.html, index.html, about.html
```

**Check 3 - Permissions?**
```bash
chmod +x start_web_app.sh
```

---

### Issue 6: Can't upload files / Upload fails

**Solutions:**

1. **Check file size:** Max 16MB
   ```bash
   ls -lh your_file.pdf
   ```

2. **Verify PDF is valid:**
   ```bash
   file your_file.pdf
   # Should say: "PDF document"
   ```

3. **Check temp directory permissions:**
   ```bash
   ls -ld /tmp
   # Should be writable
   ```

---

### Issue 7: Server starts but page is blank

**Cause:** Template rendering issue

**Solution:**
```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"

# Verify templates
python3 << 'EOF'
from web_app import app
with app.test_client() as client:
    response = client.get('/')
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.data)} bytes")
    if response.status_code != 200:
        print("Error:", response.data.decode())
EOF
```

---

## Advanced Troubleshooting

### Check What's Using Port 5000

```bash
lsof -i :5000
```

If something else is using it:
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9
```

---

### Run with Different Port

Edit `web_app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Use 8080 instead
```

Or set environment variable:
```bash
export FLASK_RUN_PORT=8080
flask run
```

---

### Enable Verbose Logging

Edit `web_app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show detailed error messages.

---

### Test Without Browser

```bash
# Test if server responds
curl http://localhost:5000

# Should return HTML content
```

---

### Check Network Settings

```bash
# Get your IP address
ifconfig | grep "inet " | grep -v 127.0.0.1

# Try accessing via IP
# http://YOUR_IP:5000
```

---

### Completely Reset Everything

```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"

# Kill any running instances
pkill -f web_app.py

# Reinstall dependencies
pip3 install --upgrade -r requirements.txt

# Restart
./start_web_app.sh
```

---

## Still Not Working?

### Diagnostic Script

Run this to check everything:

```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
python3 << 'EOFPYTHON'
import sys
import os

print("="*60)
print("DIAGNOSTIC CHECK")
print("="*60)

# 1. Python version
print(f"\n1. Python: {sys.version}")

# 2. Check imports
modules = ['flask', 'icalendar', 'PyPDF2']
for module in modules:
    try:
        __import__(module)
        print(f"✓ {module} installed")
    except ImportError:
        print(f"✗ {module} NOT installed")

# 3. Check files
files = ['web_app.py', 'travel_to_ics.py', 'templates/index.html']
for file in files:
    if os.path.exists(file):
        print(f"✓ {file} exists")
    else:
        print(f"✗ {file} missing")

# 4. Check ports
import socket
for port in [5000, 8080]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        print(f"✓ Port {port} available")
        sock.close()
    except OSError:
        print(f"✗ Port {port} in use")

# 5. Test Flask app
try:
    from web_app import app
    with app.test_client() as client:
        response = client.get('/')
        print(f"✓ Flask app works (HTTP {response.status_code})")
except Exception as e:
    print(f"✗ Flask app error: {e}")

print("="*60)
EOFPYTHON
```

---

## Contact Information

If nothing works, check:
1. The terminal output for specific error messages
2. Your Python version (`python3 --version` - needs 3.9+)
3. macOS version (needs 10.15+)

---

## Alternative: Use Command Line Instead

If the web app won't work, you can always use the command line version:

```bash
python3 travel_to_ics.py your_file.pdf output.ics
```

This bypasses the web interface entirely!

See `QUICKSTART.md` for command line instructions.

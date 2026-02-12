# 🎉 Welcome to Travel to ICS Converter!

## 🚀 Quick Start - Web Interface (Recommended)

### Step 1: Start the Server
```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
./start_web_app.sh
```

### Step 2: Open Browser
Navigate to: **http://localhost:5000**

### Step 3: Upload & Convert
1. Drag & drop your CWT PDF (or click to browse)
2. Click "Convert to Calendar"
3. Download the .ics file
4. Import to Google Calendar

**That's it!** ✨

---

## 📋 Alternative: Command Line

If you prefer the command line:

```bash
python3 travel_to_ics.py your_travel.pdf output.ics
```

---

## 📚 Documentation

### For Web App Users:
- **[WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)** - Complete web app guide
- **[README_WEB_APP.md](README_WEB_APP.md)** - Technical details

### For Command Line Users:
- **[QUICKSTART.md](QUICKSTART.md)** - Command line quick start
- **[README.md](README.md)** - Full documentation

### General:
- **[SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md)** - See example results
- **requirements.txt** - Python dependencies

---

## 🎯 What This App Does

Converts CWT travel PDFs into Google Calendar appointments with:

### For Each Flight:
- ✈️ **Flight** (with flight number, airports, reservation code)
- 🚗 **Commute & Airport** (before flight: 2.5-3.5 hours)
- 🚗 **Airport & Commute** (after flight: 1-1.5 hours)
- 🔔 **48-hour alarm** on the flight

### For Each Hotel:
- 🏨 **Hotel Stay** (check-in 3PM → check-out 12PM)
- 📍 Includes confirmation, address, phone, details
- ⏰ Marked as "free" time

### Smart Features:
- 🌍 **Automatic timezone detection** (50+ airports)
- 🔗 **Connection handling** (skips duplicate commutes)
- 🎨 **Color coding** (Flamingo for flights, Sage for hotels)

---

## ✅ System Check

Before starting, verify everything is installed:

```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
python3 -c "import flask; import icalendar; import PyPDF2; print('✅ All dependencies installed!')"
```

If you see an error, install dependencies:
```bash
pip3 install -r requirements.txt
```

---

## 🎨 Screenshots

### Web Interface:
- **Home Page**: Beautiful gradient design with drag & drop
- **Upload**: Visual feedback while processing
- **Download**: Automatic .ics file download
- **About**: Complete documentation and instructions

### Features:
- 📱 Mobile-friendly responsive design
- 🎯 Drag & drop file upload
- ⚡ Real-time processing
- 💫 Smooth animations
- ✨ Modern UI/UX

---

## 🔧 Troubleshooting

### Web App Won't Start
```bash
# Install Flask
pip3 install Flask

# Check if port is available
lsof -i :5000
```

### PDF Not Converting
- ✅ Ensure PDF is from CWT travel agents
- ✅ Check file size (max 16MB)
- ✅ Verify PDF format (Spanish CWT itinerary)

### Import to Google Calendar Fails
- ✅ Use Google Calendar website (not mobile app)
- ✅ Go to Settings → Import & Export
- ✅ Select the .ics file
- ✅ Choose destination calendar

---

## 📊 Tested With

### Sample Data:
- ✅ 3 flights (LA2696, LA4905, LA711)
- ✅ 2 hotels (Casa Andina, NH Collection)
- ✅ Multiple timezones (Chile, Peru, Colombia)
- ✅ Connection handling verified

### Browsers:
- ✅ Chrome / Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

### Platforms:
- ✅ macOS
- ✅ Linux
- ✅ Windows (with Python installed)

---

## 🎯 Next Steps

### Option 1: Try the Web Interface (Easiest)
```bash
./start_web_app.sh
```
Then open http://localhost:5000

### Option 2: Use Command Line
```bash
python3 travel_to_ics.py sample.pdf output.ics
```

### Option 3: Read the Docs
- Start with [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)
- Or [QUICKSTART.md](QUICKSTART.md) for CLI

---

## 💡 Tips

1. **Keep the terminal open** while using the web app
2. **Bookmark http://localhost:5000** for quick access
3. **Import directly** to your main Google Calendar
4. **Check the About page** in the app for detailed help

---

## 🎁 What's Included

```
📦 Travel to ICS Converter
├── 🌐 Web Interface
│   ├── Beautiful UI with drag & drop
│   ├── Mobile responsive design
│   └── Real-time processing feedback
│
├── ⌨️ Command Line Tool
│   ├── Simple Python script
│   └── Batch processing support
│
├── 📚 Documentation
│   ├── Quick start guides
│   ├── Technical details
│   └── Sample outputs
│
└── ✨ Features
    ├── Timezone support (50+ airports)
    ├── Connection handling
    ├── Color coding
    └── 48-hour flight alarms
```

---

## 🚀 Ready to Start?

### Web Interface (Recommended):
```bash
./start_web_app.sh
```

### Command Line:
```bash
python3 travel_to_ics.py your_file.pdf output.ics
```

---

**Need help?** Check the documentation files or review the terminal output for error messages.

**Enjoy converting your travel itineraries!** ✈️🏨📅

# ✨ Simplified Travel to ICS Converter

## Overview
Back to basics! Simple, focused app that does one thing really well.

## What's Included

### ✅ Core Features
- **Upload PDF** - CWT travel agent PDFs
- **Customize Colors** - 11 color options for flights & hotels
- **Customize Commute Times** - Per-airport settings
- **Download ICS** - Import to any calendar app

### ❌ What's Removed
- ~~User authentication~~
- ~~Database~~
- ~~Login/signup~~
- ~~Google Calendar direct push~~
- ~~Saved preferences~~
- ~~Profile pages~~

## Why Simplified?

**Focus**: Does one job perfectly - converts PDFs to ICS files
**Simplicity**: No accounts, no database, no complexity
**Universal**: Works with any calendar (Google, Outlook, Apple, etc.)
**Maintenance**: Much easier to maintain and deploy

## Features

### Color Customization
Choose from 11 colors for both flights and hotels:
- 🌸 Flamingo (default for flights)
- 💜 Lavender
- 💚 Sage (default for hotels)
- 🍇 Grape
- 🌸 Blossom
- 🍌 Banana
- 🌿 Basil
- 🔵 Peacock
- 🌫️ Graphite
- 💙 Blueberry
- 🍊 Tangerine

### Airport Commute Times
Customize for each major airport:
- 🇨🇱 SCL (Santiago)
- 🇦🇷 AEP (Buenos Aires - Aeroparque)
- 🇦🇷 EZE (Buenos Aires - Ezeiza)
- 🇧🇷 GRU (São Paulo)
- 🇲🇽 MEX (Mexico City)
- 🌍 International (default for others)

**Before departure**: 2.0 - 5.0 hours
**After landing**: 0.5 - 3.0 hours

## Deployment

### Requirements
- Flask
- PyPDF2
- icalendar
- gunicorn
- python-dotenv

**No database needed!** ✅

### Environment Variables
Only one required:
```
SECRET_KEY=<any random string>
```

Generate with:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### On Render
1. ✅ No PostgreSQL needed
2. ✅ Just set SECRET_KEY
3. ✅ Deploy and done!

## User Flow

1. Visit app
2. Upload PDF
3. (Optional) Customize colors and times
4. Click "Convert to Calendar"
5. Download ICS file
6. Import to any calendar app
7. Done! ✅

## Technical Details

### Files
- `web_app_production.py` - Main Flask app (simplified)
- `requirements-production.txt` - Minimal dependencies
- `travel_to_ics.py` - PDF parser
- `custom_ics_generator.py` - ICS generator with customization
- `templates/index.html` - Upload form with settings
- `templates/base.html` - Base template
- `templates/about.html` - Instructions

### No Longer Needed
- ~~database.py~~
- ~~auth.py~~
- ~~login/register templates~~
- ~~Flask-SQLAlchemy~~
- ~~Flask-Login~~
- ~~psycopg2~~
- ~~Google Calendar integration~~

## Benefits

### For Users
- ✅ No account required
- ✅ No personal data stored
- ✅ Works offline (after download)
- ✅ Import to any calendar
- ✅ One-time use or repeated use
- ✅ Fast and simple

### For Deployment
- ✅ No database to manage
- ✅ Stateless (scales easily)
- ✅ Fewer dependencies
- ✅ Lower resource usage
- ✅ Easier debugging
- ✅ Simpler updates

### For Maintenance
- ✅ Less code to maintain
- ✅ Fewer breaking changes
- ✅ No user data concerns
- ✅ No GDPR complications
- ✅ Clear, focused purpose

## Testing

### Local
```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
python3 web_app_production.py
# Visit: http://localhost:8080
```

### Production
Visit: https://travel-to-ics-converter.onrender.com

### Health Check
```bash
curl https://travel-to-ics-converter.onrender.com/health
```

Expected:
```json
{
  "status": "healthy",
  "service": "travel-to-ics",
  "features": {
    "ics_download": true,
    "customization": true
  }
}
```

## Future Possibilities

If needed later, could add:
- Multiple PDF uploads at once
- Save settings in browser (localStorage)
- More airports
- More color options
- Email delivery of ICS files
- API endpoint

But for now: **Simple is better!**

## Summary

**What it does**: Converts CWT travel PDFs to ICS calendar files
**How it works**: Upload, customize (optional), download
**Where it works**: Any calendar app
**Who can use it**: Anyone, no account needed
**Cost**: Free (minimal resources)

---

**Philosophy**: Do one thing, do it well, make it simple.

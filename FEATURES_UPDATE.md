# 🎨 New Features Added!

## ✨ Customizable Colors

You can now choose custom colors for your calendar events!

### Flight & Commute Colors
Choose from 11 Google Calendar colors:
- 🌸 Flamingo (Default) - Orange/pink
- 💜 Lavender - Purple
- 💚 Sage - Green
- 🍇 Grape - Purple
- 🌸 Blossom - Pink
- 🍌 Banana - Yellow
- 🌿 Basil - Green
- 🔵 Peacock - Blue
- 🌫️ Graphite - Gray
- 💙 Blueberry - Blue
- 🍊 Tangerine - Orange

### Hotel Colors
Same color options as above!

**Default:** Sage (green) for hotels

---

## 🚗 Customizable Airport Commute Times

### Major Airports Supported

**Before Departure:**
- 🇨🇱 **SCL** (Santiago) - Default: 2.5 hours
- 🇦🇷 **AEP** (Buenos Aires) - Default: 3.5 hours
- 🇦🇷 **EZE** (Buenos Aires Intl) - Default: 3.5 hours
- 🇧🇷 **GRU** (São Paulo) - Default: 3.5 hours
- 🇲🇽 **MEX** (Mexico City) - Default: 3.5 hours
- 🌍 **Other International** - Default: 3.5 hours

**After Landing:**
- 🇨🇱 **SCL** (Santiago) - Default: 1 hour
- 🇦🇷 **AEP** (Buenos Aires) - Default: 1 hour
- 🇦🇷 **EZE** (Buenos Aires Intl) - Default: 1.5 hours
- 🇧🇷 **GRU** (São Paulo) - Default: 1.5 hours
- 🇲🇽 **MEX** (Mexico City) - Default: 1.5 hours
- 🌍 **Other International** - Default: 1.5 hours

### Customization Options

Each airport time can be adjusted:
- **Before:** 2.0 - 5.0 hours
- **After:** 0.5 - 3.0 hours

---

## 🎯 How to Use

1. **Upload your PDF** - Drag & drop or click to select
2. **Customize settings** - Options appear after file selection
3. **Choose colors** - Select your preferred calendar colors
4. **Adjust commute times** - Fine-tune based on your preferences
5. **Convert** - Click the button to generate your ICS file

---

## 📱 Where to Find It

Visit: https://travel-to-ics-converter.onrender.com

Upload a PDF and you'll see the customization panel!

---

## 🔄 Updates Applied

**Frontend:**
- ⚙️ New customization panel (appears after file selection)
- 🎨 Color picker dropdowns with emojis
- 🚗 Airport-specific commute time selectors
- 📊 Grid layout for easy comparison

**Backend:**
- 🧩 New `CustomICSGenerator` class
- 🎯 Dynamic color application
- ⏱️ Custom commute duration logic
- 🔧 Form data processing

**Default Behavior:**
- ✅ All defaults match previous behavior
- ✅ No breaking changes
- ✅ Backwards compatible

---

## 💡 Example Use Cases

### Short Domestic Trips
- Set SCL commute to 2 hours (instead of 2.5)
- Perfect for frequent travelers

### International Connections
- Set international before time to 4 hours
- Extra buffer for customs/immigration

### Rush Hour Considerations
- Increase GRU/MEX times during peak hours
- Account for traffic patterns

### Quick Connections
- Reduce after-landing time for familiar airports
- Save calendar space

---

## 🎨 Color Recommendations

**Work Travel:**
- Flights: Blue or Purple
- Hotels: Green (for work/money saved)

**Vacation:**
- Flights: Orange or Yellow (bright and happy!)
- Hotels: Pink or Lavender

**Mixed Trips:**
- Keep defaults (Flamingo for flights, Sage for hotels)

---

## 🔧 Technical Details

**New Files:**
- `custom_ics_generator.py` - Extended ICS generator
- Updated `templates/index.html` - New UI

**Updated Files:**
- `web_app.py` - Local development
- `web_app_production.py` - Production deployment

**Deployment:**
- ✅ Pushed to GitHub
- ✅ Auto-deploying to Render
- ⏱️ Live in 2-3 minutes

---

## 🚀 Try It Now!

1. Go to: https://travel-to-ics-converter.onrender.com
2. Upload your sample PDF
3. Play with the color options!
4. Adjust commute times
5. See the difference in your calendar

---

## 📊 Statistics

**Lines of Code Added:** ~200+
**New Features:** 2 major (colors + times)
**Customization Options:** 23 total
**Color Choices:** 11 per event type
**Airport-Specific Settings:** 10 dropdowns

---

**Enjoy your new customization options!** 🎉

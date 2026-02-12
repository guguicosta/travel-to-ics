# 📖 User Guide - Travel to ICS Converter

Welcome! This app converts your CWT travel agent PDF files into calendar events.

---

## 🎯 Quick Start

### Step 1: Upload Your PDF
- Drag & drop your PDF file, or
- Click to browse and select your file
- ✅ Supported: CWT travel agent PDF files

### Step 2: Choose Output Method

You now have **two options**:

#### 🔵 Option A: Download ICS File
**Best for**: Anyone who wants to import events manually

**Pros**:
- ✅ Works with any calendar app (Google, Outlook, Apple, etc.)
- ✅ No authentication needed
- ✅ Quick and simple

**How it works**:
1. Select this option
2. Choose your colors and times
3. Click "Convert"
4. Download the .ics file
5. Import it to your calendar app

---

#### 🟢 Option B: Push to Google Calendar
**Best for**: Google Calendar users who want instant results

**Pros**:
- ✅ Events created automatically
- ✅ No manual import needed
- ✅ Faster workflow

**Requires**:
- ⚠️ Google account
- ⚠️ One-time authorization

**How it works**:
1. Select this option
2. Choose your colors and times
3. Click "Convert"
4. Sign in with Google (first time only)
5. Grant calendar permission
6. Done! Events appear in your calendar

---

### Step 3: Customize Your Events

#### Choose Colors

**For Flights & Commutes**:
- 🌸 Flamingo (Orange/Pink) - Default
- 💜 Lavender
- 💚 Sage
- 🍇 Grape
- 🌸 Blossom
- 🍌 Banana
- 🌿 Basil
- 🔵 Peacock
- 🌫️ Graphite
- 💙 Blueberry
- 🍊 Tangerine

**For Hotels**:
Same color options as above!
- Default: 💚 Sage (Green)

**Tip**: Use different colors for work vs. personal trips!

---

#### Adjust Airport Commute Times

**Before Departure** (time to arrive at airport before flight):

| Airport | Default | Range |
|---------|---------|-------|
| 🇨🇱 SCL (Santiago) | 2.5 hours | 2.0 - 5.0 |
| 🇦🇷 AEP (Buenos Aires) | 3.5 hours | 2.0 - 5.0 |
| 🇦🇷 EZE (Buenos Aires Intl) | 3.5 hours | 2.0 - 5.0 |
| 🇧🇷 GRU (São Paulo) | 3.5 hours | 2.0 - 5.0 |
| 🇲🇽 MEX (Mexico City) | 3.5 hours | 2.0 - 5.0 |
| 🌍 Other International | 3.5 hours | 2.0 - 5.0 |

**After Landing** (time to leave airport after arrival):

| Airport | Default | Range |
|---------|---------|-------|
| 🇨🇱 SCL (Santiago) | 1.0 hour | 0.5 - 3.0 |
| 🇦🇷 AEP (Buenos Aires) | 1.0 hour | 0.5 - 3.0 |
| 🇦🇷 EZE (Buenos Aires Intl) | 1.5 hours | 0.5 - 3.0 |
| 🇧🇷 GRU (São Paulo) | 1.5 hours | 0.5 - 3.0 |
| 🇲🇽 MEX (Mexico City) | 1.5 hours | 0.5 - 3.0 |
| 🌍 Other International | 1.5 hours | 0.5 - 3.0 |

**Tip**: Adjust based on your familiarity with the airport!

---

## ✈️ What Events Are Created?

For each flight, you get **THREE events**:

### 1. Commute to Airport
- 📍 Starts X hours before departure
- ⏰ Ends at flight departure time
- 🎨 Same color as flight
- 🔔 No alarm

### 2. Flight
- ✈️ From departure to arrival
- 🌍 Separate timezones for departure/arrival
- 🎨 Your chosen flight color
- 🔔 48-hour reminder
- 📝 Includes reservation code and ticket number

### 3. Commute from Airport
- 📍 Starts at landing time
- ⏰ Ends X hours after arrival
- 🎨 Same color as flight
- 🔔 No alarm

**Smart Connection Detection**:
- If flights are < 12 hours apart at same airport
- Only one commute event created (not two)

---

## 🏨 Hotel Events

For each hotel, you get **ONE event**:

- 🏨 Name as title
- 📅 Check-in: 3:00 PM on arrival day
- 📅 Check-out: 12:00 PM on departure day
- 🎨 Your chosen hotel color
- 🔔 No alarms
- 📝 Includes confirmation, address, and phone

---

## 💡 Tips & Tricks

### Color Coding Ideas

**Work Travel**:
- Flights: 🔵 Blue or 💜 Purple
- Hotels: 💚 Green

**Vacation**:
- Flights: 🍊 Orange or 🍌 Yellow
- Hotels: 🌸 Pink or 💜 Lavender

**Mixed Trips**:
- Use defaults (easy to remember)

---

### Commute Time Recommendations

**Shorter Times** (experienced travelers):
- SCL: 2.0 hours before
- Familiar airports: 0.5 hours after

**Longer Times** (safe buffer):
- International: 4.0 hours before
- Peak traffic: 2.0 hours after

**Rush Hour Considerations**:
- GRU/MEX morning flights: +0.5 hours
- EZE afternoon flights: +1.0 hour

---

## 🔐 First Time Using Google Calendar Push?

When you select "Push to Google Calendar" for the first time:

1. **You'll be redirected to Google**
   - This is normal and expected

2. **Sign in with your Google account**
   - Use the account that has your calendar

3. **You'll see a permission request**
   - App name: "Travel to ICS Converter"
   - Permission: "Create events in your calendar"

4. **Click "Allow"**
   - App can only CREATE events
   - Cannot read or delete existing events
   - You can revoke access anytime

5. **You'll be redirected back**
   - Events are created automatically
   - You'll see a success message

**Future uploads**: No need to authorize again! Events are pushed instantly.

---

## ❓ FAQ

### Q: What calendar apps work with ICS download?
**A**: All of them! Google Calendar, Outlook, Apple Calendar, Thunderbird, etc.

### Q: What if I don't have a Google account?
**A**: Use the "Download ICS File" option instead. It works with any calendar.

### Q: Can I use both methods?
**A**: Yes! Upload your PDF twice and choose different methods.

### Q: How do I revoke Google Calendar access?
**A**: Go to [Google Account Permissions](https://myaccount.google.com/permissions) and remove "Travel to ICS Converter".

### Q: What happens to my PDF file?
**A**: It's deleted immediately after processing. We don't store your files.

### Q: Can I change event colors later?
**A**: Yes! In Google Calendar, click the event → Edit → Choose color.

### Q: What if my PDF isn't recognized?
**A**: Make sure it's a CWT travel agent PDF in Spanish format. Contact support if issues persist.

### Q: Do hotel events block my time?
**A**: No, they show as "Free" (transparent) so you can schedule meetings during your stay.

### Q: Why 48 hours for flight alarms?
**A**: Standard recommendation to prepare for travel (packing, arrangements, etc.).

### Q: Can I customize alarm times?
**A**: After import, edit events in your calendar to change alarm times.

---

## 🆘 Troubleshooting

### ICS Download Issues

**Problem**: Download doesn't start
- **Solution**: Check pop-up blocker settings

**Problem**: Events don't import to calendar
- **Solution**: Make sure you're opening the .ics file with your calendar app

**Problem**: Events appear in wrong timezone
- **Solution**: The app uses correct airport timezones - your calendar should adjust automatically

---

### Google Calendar Issues

**Problem**: "App not verified" warning
- **Solution**: This is normal for apps in testing mode. Click "Advanced" → "Go to Travel to ICS Converter"

**Problem**: Authorization fails
- **Solution**: Make sure you're using a personal Google account (not restricted work account)

**Problem**: Events created but wrong color
- **Solution**: Google Calendar sometimes takes a few seconds to apply colors. Refresh the page.

**Problem**: Duplicate events created
- **Solution**: Don't upload the same PDF twice with Google Calendar method (it creates new events each time)

---

## 📞 Support

**Issues?**
- Check this guide first
- Review [GOOGLE_CALENDAR_SETUP.md](./GOOGLE_CALENDAR_SETUP.md) for API issues
- Contact your administrator

**Feature Requests?**
- Share your ideas!
- What would make this app better for you?

---

## 🎉 Enjoy Your Organized Travel Calendar!

Happy travels! ✈️🌍🏨

---

*Last Updated: February 12, 2026*

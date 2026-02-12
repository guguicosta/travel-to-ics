# ✅ Google Calendar API Setup Checklist

Follow these steps in order. Check off each one as you complete it!

---

## 🎯 Step 1: Create Google Cloud Project

- [ ] Go to https://console.cloud.google.com/
- [ ] Click "Select a project" (top of page)
- [ ] Click "New Project"
- [ ] Enter name: **Travel ICS Converter**
- [ ] Click **Create**
- [ ] Wait for project to be created (notification will appear)

✅ **Done?** Move to Step 2!

---

## 🎯 Step 2: Enable Google Calendar API

- [ ] Make sure your new project is selected (check top bar)
- [ ] Click hamburger menu (☰) → **APIs & Services** → **Library**
- [ ] In the search box, type: **Google Calendar API**
- [ ] Click on **Google Calendar API** in results
- [ ] Click the blue **Enable** button
- [ ] Wait for "API enabled" confirmation

✅ **Done?** Move to Step 3!

---

## 🎯 Step 3: Configure OAuth Consent Screen

- [ ] Click hamburger menu (☰) → **APIs & Services** → **OAuth consent screen**
- [ ] Select **External** user type
- [ ] Click **Create**

### Fill in App Information:
- [ ] **App name**: `Travel to ICS Converter`
- [ ] **User support email**: Your email (select from dropdown)
- [ ] **App logo**: Leave blank (optional)
- [ ] **App domain**: Leave blank (optional)
- [ ] **Authorized domains**: Leave blank (optional)
- [ ] **Developer contact email**: Your email
- [ ] Click **Save and Continue**

### Scopes Page:
- [ ] Don't add any scopes (the app will request them automatically)
- [ ] Click **Save and Continue**

### Test Users Page:
- [ ] Click **Add Users**
- [ ] Enter your email address
- [ ] Click **Add**
- [ ] Click **Save and Continue**

### Summary Page:
- [ ] Review the information
- [ ] Click **Back to Dashboard**

✅ **Done?** Move to Step 4!

---

## 🎯 Step 4: Create OAuth Credentials

- [ ] Click hamburger menu (☰) → **APIs & Services** → **Credentials**
- [ ] Click **+ Create Credentials** (top of page)
- [ ] Select **OAuth client ID**

### Configure OAuth Client:
- [ ] **Application type**: Select **Web application**
- [ ] **Name**: `Travel ICS Web App`

### Authorized Redirect URIs:
- [ ] Click **+ Add URI**
- [ ] Enter: `http://localhost:8080/google-callback`
- [ ] Click **+ Add URI** again
- [ ] Enter: `https://travel-to-ics-converter.onrender.com/google-callback`

  ⚠️ **Important**: Replace `travel-to-ics-converter` with your actual Render app name if different!

- [ ] Click **Create**

### Download Credentials:
- [ ] A popup appears with Client ID and Client Secret
- [ ] Click **Download JSON** button
- [ ] Save the file to your Downloads folder

✅ **Done?** Move to Step 5!

---

## 🎯 Step 5: Install Credentials Locally

Now let's move the credentials file to the right place:

### Option A: Manual Move (Easier)
```bash
# 1. Find the downloaded file in your Downloads folder
# It's named something like: client_secret_XXXXX.json

# 2. Rename and move it:
mv ~/Downloads/client_secret_*.json "/Users/agcosta/Proyecto Claude EA viajes/credentials.json"
```

### Option B: Interactive
- [ ] Open Finder
- [ ] Go to Downloads folder
- [ ] Find file starting with `client_secret_`
- [ ] Rename it to `credentials.json`
- [ ] Move it to: `/Users/agcosta/Proyecto Claude EA viajes/`

### Verify Installation:
```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
python3 check_setup.py
```

**Expected output**:
```
✓ credentials.json: ✅ Found
✅ Google Calendar integration is configured!
```

✅ **Done?** Move to Step 6!

---

## 🎯 Step 6: Test Locally

Let's make sure everything works on your computer first:

- [ ] Open terminal
- [ ] Run the app:
  ```bash
  cd "/Users/agcosta/Proyecto Claude EA viajes"
  python3 web_app_production.py
  ```
- [ ] Open browser to: http://localhost:8080
- [ ] Upload your sample PDF
- [ ] Select **"Push to Google Calendar"** option
- [ ] Choose colors/times if desired
- [ ] Click **Convert**
- [ ] You'll be redirected to Google
- [ ] Sign in with your Google account (if not already signed in)
- [ ] You'll see: "Google hasn't verified this app" ← **This is normal!**
- [ ] Click **Advanced** → **Go to Travel to ICS Converter (unsafe)**
- [ ] Review permissions
- [ ] Click **Allow**
- [ ] You'll be redirected back to the app
- [ ] Check for success message
- [ ] Open Google Calendar and verify events were created!

✅ **All events created successfully?** Move to Step 7!

---

## 🎯 Step 7: Deploy to Production (Render.com)

Now we need to make the credentials available on Render:

### Get Your Render App Name:
- [ ] Go to https://dashboard.render.com/
- [ ] Click on your **travel-to-ics** service
- [ ] Note the app URL (e.g., `https://travel-to-ics-converter.onrender.com`)
- [ ] Your app name is the part before `.onrender.com`

### Verify Redirect URI:
- [ ] Go back to Google Cloud Console
- [ ] Navigate to **APIs & Services** → **Credentials**
- [ ] Click on your **Travel ICS Web App** OAuth client
- [ ] Under **Authorized redirect URIs**, verify you have:
  - `https://YOUR-APP-NAME.onrender.com/google-callback`
- [ ] If not, add it now and click **Save**

### Upload Credentials to Render:

**Option A: Environment Variable (Recommended for Production)**
```bash
# 1. Convert credentials to base64
cd "/Users/agcosta/Proyecto Claude EA viajes"
cat credentials.json | base64 | pbcopy
# This copies the base64 string to your clipboard
```

- [ ] Go to Render dashboard
- [ ] Click your app → **Environment**
- [ ] Click **Add Environment Variable**
- [ ] Key: `GOOGLE_CREDENTIALS_JSON`
- [ ] Value: Paste the base64 string (Cmd+V)
- [ ] Click **Save Changes**

**Option B: Direct File Upload (Simpler, but may be lost on redeploy)**

We need to update the app to look for credentials in the environment variable. For now, let's use the simpler option:

- [ ] Go to Render dashboard
- [ ] Click your app → **Shell** (in the left menu)
- [ ] Wait for shell to connect
- [ ] Run:
  ```bash
  cat > credentials.json
  ```
- [ ] Paste the entire contents of your credentials.json file
- [ ] Press Ctrl+D to save
- [ ] Type `exit` to close shell

### Redeploy:
- [ ] Render will automatically redeploy when you save environment variables
- [ ] OR manually redeploy: Click **Manual Deploy** → **Deploy latest commit**
- [ ] Wait for deployment to complete (2-3 minutes)

✅ **Done?** Move to Step 8!

---

## 🎯 Step 8: Test Production

Final test on the live site!

- [ ] Go to your production URL: https://travel-to-ics-converter.onrender.com
- [ ] Upload a PDF
- [ ] Select **"Push to Google Calendar"**
- [ ] Click **Convert**
- [ ] Complete Google authorization (same steps as local test)
- [ ] Verify events are created in your calendar

### Check Feature Status:
```bash
curl https://travel-to-ics-converter.onrender.com/health
```

**Expected output**:
```json
{
  "status": "healthy",
  "service": "travel-to-ics",
  "features": {
    "ics_download": true,
    "google_calendar": true  ← Should be true!
  }
}
```

✅ **Everything working?** You're done! 🎉

---

## 🎊 Success!

You now have:
- ✅ ICS download (works for everyone)
- ✅ Google Calendar push (works after authorization)
- ✅ Full customization (colors, commute times)

### Share with Colleagues:
Send them: https://travel-to-ics-converter.onrender.com

They can use either:
1. **Download ICS File** - No authorization needed
2. **Push to Google Calendar** - One-time authorization

---

## 🆘 Troubleshooting

### "redirect_uri_mismatch" error
→ Double-check the redirect URI in Google Cloud Console matches exactly

### "Access Blocked: Authorization Error"
→ Make sure you added yourself as a test user in OAuth consent screen

### Events not appearing in calendar
→ Check Google Calendar web interface (may take a few seconds to sync)

### Still having issues?
Run diagnostics:
```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
python3 check_setup.py
```

---

**Questions?** Re-read GOOGLE_CALENDAR_SETUP.md for detailed explanations!

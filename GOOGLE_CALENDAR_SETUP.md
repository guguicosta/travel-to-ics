# 🔐 Google Calendar Integration Setup

This guide will help you set up Google Calendar API credentials for the direct push feature.

## 📋 Prerequisites

- Google Account
- Access to Google Cloud Console

## 🚀 Setup Steps

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: `Travel ICS Converter` (or your preferred name)
4. Click "Create"

### 2. Enable Google Calendar API

1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for "Google Calendar API"
3. Click on it and press **Enable**

### 3. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** user type
3. Click **Create**
4. Fill in the required information:
   - **App name**: Travel to ICS Converter
   - **User support email**: Your email
   - **Developer contact email**: Your email
5. Click **Save and Continue**
6. On the "Scopes" page, click **Save and Continue** (no need to add scopes manually)
7. On "Test users" page, click **Add Users** and add your email
8. Click **Save and Continue**

### 4. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select **Application type**: Web application
4. Enter **Name**: Travel ICS Web App
5. Under **Authorized redirect URIs**, add:
   - For local testing: `http://localhost:8080/google-callback`
   - For production: `https://your-app-name.onrender.com/google-callback`

   ⚠️ **Important**: Replace `your-app-name` with your actual Render app name!

6. Click **Create**
7. You'll see a popup with Client ID and Client Secret - **download the JSON file**

### 5. Save Credentials File

1. Rename the downloaded file to `credentials.json`
2. Place it in your project root directory: `/Users/agcosta/Proyecto Claude EA viajes/credentials.json`

⚠️ **Security Warning**: Never commit `credentials.json` to GitHub!

### 6. Update .gitignore

Make sure your `.gitignore` includes:
```
credentials.json
token.pickle
*.pickle
```

## 🔧 Deployment Configuration

### For Render.com Deployment

You'll need to set the credentials as an environment variable or upload the file:

**Option 1: Environment Variable (Recommended)**
1. Convert `credentials.json` to base64:
   ```bash
   cat credentials.json | base64
   ```
2. In Render dashboard → Environment → Add:
   - Key: `GOOGLE_CREDENTIALS_JSON`
   - Value: [paste the base64 string]

3. Update `google_calendar_integration.py` to read from environment variable

**Option 2: File Upload**
1. In Render dashboard, use the Shell to upload the file
2. Not recommended as files may be lost on redeploy

## 🧪 Testing

### Local Testing

1. Make sure `credentials.json` is in the project root
2. Run the app locally:
   ```bash
   python web_app_production.py
   ```
3. Upload a PDF and select "Push to Google Calendar"
4. You'll be redirected to Google for authorization
5. Accept the permissions
6. Events should be created in your calendar!

### Production Testing

1. Deploy to Render with credentials configured
2. Update the OAuth redirect URI to match your production URL
3. Test the same workflow on the live site

## 📝 Important Notes

- **First-time authorization**: Users will see a warning that the app is not verified by Google. This is normal for apps in testing mode.
- **Token storage**: User tokens are stored in `token.pickle` - in production, consider using a database
- **Scope**: The app only requests `calendar.events` scope (create/edit events)
- **Privacy**: The app never reads existing calendar events, only creates new ones

## 🔒 Security Best Practices

1. ✅ Never commit `credentials.json` to version control
2. ✅ Use environment variables in production
3. ✅ Keep `token.pickle` files secure
4. ✅ Regularly rotate client secrets if compromised
5. ✅ Monitor OAuth usage in Google Cloud Console

## 🆘 Troubleshooting

### "redirect_uri_mismatch" Error
- Make sure the redirect URI in Google Cloud Console exactly matches your app's callback URL
- Include both `http://localhost:8080/google-callback` for local and production URL

### "invalid_grant" Error
- Delete `token.pickle` and re-authorize
- Check that credentials haven't expired

### "Access Blocked: Authorization Error"
- Make sure you added your email as a test user in OAuth consent screen
- If app is not published, only test users can authorize

## 🎉 You're All Set!

Once configured, users can:
1. Upload their PDF
2. Choose "Push to Google Calendar"
3. Authorize once
4. Events are created automatically!

---

**Need help?** Check the [Google Calendar API Documentation](https://developers.google.com/calendar/api/quickstart/python)

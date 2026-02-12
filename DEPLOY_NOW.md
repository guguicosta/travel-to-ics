# 🚀 Deploy Your App - Quick Start

## Easiest Way: One-Click Heroku Deployment

### Step 1: Install Heroku CLI

```bash
brew tap heroku/brew && brew install heroku
```

Or download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Run Deployment Script

```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
./deploy_heroku.sh
```

The script will:
1. ✅ Check if Heroku CLI is installed
2. ✅ Login to Heroku (opens browser)
3. ✅ Create a new app
4. ✅ Generate secure secret key
5. ✅ Setup git repository
6. ✅ Deploy your app
7. ✅ Test the deployment
8. ✅ Give you the public URL

**Total time: 5-10 minutes** ⏱️

---

## Your App Will Be Live At:

`https://your-app-name.herokuapp.com`

**Share this URL** with anyone you want to use the app! 🎉

---

## Alternative: Manual Deployment

If you prefer to do it manually:

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
cd "/Users/agcosta/Proyecto Claude EA viajes"
heroku create your-app-name

# 3. Set secret key
heroku config:set SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# 4. Copy production requirements
cp requirements-production.txt requirements.txt

# 5. Initialize git and deploy
git init
git add .
git commit -m "Deploy Travel to ICS"
git push heroku main

# 6. Open your app
heroku open
```

---

## What People Will See

When someone visits your public URL:

1. **Beautiful web interface** with drag & drop
2. **Upload their CWT PDF** file
3. **Get ICS file** downloaded automatically
4. **Import to Google Calendar** - done!

---

## Free Tier Limits

Heroku free tier includes:
- ✅ 550 hours per month (basically always on)
- ✅ Automatic HTTPS
- ✅ No credit card required initially
- ⚠️ Sleeps after 30 min of inactivity (wakes up in ~10 seconds)

**This is perfect for sharing with friends and colleagues!**

---

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Updated app"
git push heroku main
```

---

## Monitoring

Check if your app is running:
```bash
curl https://your-app-name.herokuapp.com/health
```

View logs:
```bash
heroku logs --tail
```

---

## Other Deployment Options

See `DEPLOYMENT_GUIDE.md` for:
- Google Cloud Platform
- Railway
- Render
- Vercel
- Docker
- And more!

---

## 🆘 Need Help?

1. **Read full guide:** `DEPLOYMENT_GUIDE.md`
2. **Heroku docs:** https://devcenter.heroku.com
3. **Check logs:** `heroku logs --tail`

---

## ✅ Quick Checklist

Before deploying:
- [ ] Heroku CLI installed
- [ ] In project directory
- [ ] Ready to login to Heroku account

After deploying:
- [ ] App URL works
- [ ] Can upload a PDF
- [ ] ICS file downloads
- [ ] Shared URL with others

---

**Ready? Just run:**

```bash
./deploy_heroku.sh
```

🎉 **In 10 minutes, your app will be live and shareable!** 🎉

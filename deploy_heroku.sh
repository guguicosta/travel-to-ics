#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🚀 Heroku Deployment Script - Travel to ICS             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found!"
    echo ""
    echo "Please install it first:"
    echo "  brew tap heroku/brew && brew install heroku"
    echo ""
    echo "Or download from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✓ Heroku CLI found"
echo ""

# Check if logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "📝 Please login to Heroku..."
    heroku login
fi

echo "✓ Logged in to Heroku"
echo ""

# Get app name
read -p "Enter a name for your app (or press Enter for auto-generated): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "🎲 Creating app with auto-generated name..."
    HEROKU_OUTPUT=$(heroku create 2>&1)
else
    echo "🎲 Creating app: $APP_NAME..."
    HEROKU_OUTPUT=$(heroku create "$APP_NAME" 2>&1)
fi

echo "$HEROKU_OUTPUT"
APP_URL=$(echo "$HEROKU_OUTPUT" | grep -o 'https://[^ ]*herokuapp.com' | head -1)

if [ -z "$APP_URL" ]; then
    echo "❌ Failed to create app. It may already exist."
    read -p "Enter your existing app name: " EXISTING_APP
    APP_NAME=$EXISTING_APP
    APP_URL="https://$APP_NAME.herokuapp.com"
fi

echo ""
echo "✓ App created: $APP_URL"
echo ""

# Generate and set secret key
echo "🔑 Generating secure SECRET_KEY..."
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set SECRET_KEY="$SECRET_KEY" -a "$APP_NAME"
echo "✓ SECRET_KEY configured"
echo ""

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Git initialized"
    echo ""
fi

# Add .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.env
.venv
venv/
ENV/
*.ics
*.pdf
.DS_Store
EOF
    echo "✓ Created .gitignore"
fi

# Copy production requirements
cp requirements-production.txt requirements.txt
echo "✓ Using production requirements"
echo ""

# Add files
echo "📦 Adding files to git..."
git add .
git commit -m "Deploy Travel to ICS Converter to Heroku" 2>/dev/null || git commit --amend --no-edit

echo "✓ Files committed"
echo ""

# Add Heroku remote if it doesn't exist
if ! git remote | grep -q heroku; then
    heroku git:remote -a "$APP_NAME"
    echo "✓ Added Heroku remote"
fi

# Deploy
echo "🚀 Deploying to Heroku..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

git push heroku main || git push heroku master

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check deployment
echo "🔍 Checking deployment status..."
sleep 3

if curl -s "$APP_URL/health" | grep -q "healthy"; then
    echo "✓ App is healthy and running!"
else
    echo "⚠️  App deployed but health check failed. Checking logs..."
    heroku logs --tail -n 50 -a "$APP_NAME"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 DEPLOYMENT SUCCESS! 🎉                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Your app is live at:"
echo "   $APP_URL"
echo ""
echo "📱 Share this URL with your friends and colleagues!"
echo ""
echo "🔧 Useful commands:"
echo "   View logs:    heroku logs --tail -a $APP_NAME"
echo "   Open app:     heroku open -a $APP_NAME"
echo "   App info:     heroku info -a $APP_NAME"
echo "   Restart:      heroku restart -a $APP_NAME"
echo ""
echo "📝 To update your app later:"
echo "   git add ."
echo "   git commit -m 'Update app'"
echo "   git push heroku main"
echo ""
echo "═══════════════════════════════════════════════════════════════"

# Open in browser
read -p "Open app in browser now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    heroku open -a "$APP_NAME"
fi

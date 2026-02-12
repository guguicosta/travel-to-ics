#!/usr/bin/env python3
"""
Check if Google Calendar integration is properly configured
"""

import os
import sys

def check_setup():
    """Check if all required files are present for Google Calendar integration"""

    print("=" * 60)
    print("  Google Calendar Integration Setup Check")
    print("=" * 60)
    print()

    # Check credentials.json
    credentials_exists = os.path.exists('credentials.json')
    print(f"✓ credentials.json: {'✅ Found' if credentials_exists else '❌ Missing'}")

    if not credentials_exists:
        print()
        print("⚠️  Google Calendar integration is NOT configured")
        print()
        print("To enable Google Calendar push feature:")
        print("1. Follow the guide in GOOGLE_CALENDAR_SETUP.md")
        print("2. Download credentials.json from Google Cloud Console")
        print("3. Place it in the project root directory")
        print()
        print("📝 Read the full guide: GOOGLE_CALENDAR_SETUP.md")
        print()
        print("💡 In the meantime, users can use the 'Download ICS File' option")
        print("   which works with any calendar app!")
        return False
    else:
        print()
        print("✅ Google Calendar integration is configured!")
        print()
        print("Users can now:")
        print("  • Download ICS files (works with any calendar)")
        print("  • Push directly to Google Calendar (OAuth2)")
        return True

if __name__ == '__main__':
    success = check_setup()
    sys.exit(0 if success else 1)

# Quick Start Guide

## Installation

```bash
cd "/Users/agcosta/Proyecto Claude EA viajes"
pip3 install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python3 travel_to_ics.py <path_to_pdf> [output_file.ics]
```

### Example

```bash
python3 travel_to_ics.py ~/Downloads/my_trip.pdf my_trip.ics
```

If you don't specify an output file, it will create `travel_calendar.ics` in the current directory.

## Import to Google Calendar

1. Open [Google Calendar](https://calendar.google.com)
2. Click the **gear icon** (Settings) → **Import & Export**
3. Click **Select file from your computer**
4. Choose the generated `.ics` file
5. Select the destination calendar
6. Click **Import**

## What Gets Created

For each flight, you'll get **3 appointments**:
- 🚗 **Commute & Airport** (before flight) - Flamingo color
- ✈️ **Flight** (with 48-hour alarm) - Flamingo color
- 🚗 **Airport & Commute** (after flight) - Flamingo color

For each hotel, you'll get **1 appointment**:
- 🏨 **Hotel Stay** (check-in to check-out, marked as "free") - Sage color

## Troubleshooting

### "ModuleNotFoundError: No module named 'PyPDF2'"
Run the installation command again:
```bash
pip3 install -r requirements.txt
```

### "No such file or directory"
Make sure the PDF path is correct. You can drag and drop the file into Terminal to get the full path.

### Dates are wrong
The app is designed for CWT travel agent PDFs. If you're using a different format, the parsing may not work correctly.

### Missing hotels or flights
Check the console output - it will show which items were successfully parsed and which had issues.

## Example Output

See `SAMPLE_OUTPUT.md` for a detailed example of what was generated from a real CWT itinerary.

## Color Codes in Google Calendar

- **Flamingo (11)**: All flight and commute appointments
- **Sage (6)**: All hotel appointments

These colors are automatically applied when you import the ICS file.

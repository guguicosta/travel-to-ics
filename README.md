# Travel PDF to ICS Calendar Converter

Converts travel agent PDFs into Google Calendar ICS files with automatic flight and hotel appointments.

## Features

### Flight Appointments
- **Flight Event**: Includes flight number, origin → destination airports
  - Uses correct timezones for departure and arrival cities
  - Includes reservation code and ticket number in description
  - 48-hour advance alarm
  - Flamingo color (Google Calendar color code 11)

- **Commute & Airport (Before Flight)**:
  - Ends at flight departure time
  - Duration: 2.5 hours for SCL, 3.5 hours for other airports
  - Flamingo color

- **Airport & Commute (After Flight)**:
  - Starts at flight arrival time
  - Duration: 1 hour for AEP/SCL, 1.5 hours for other airports
  - Flamingo color

### Connection Handling
For connecting flights with less than 12 hours between them at the same airport:
- Only creates "Commute & Airport" for the first leg
- Only creates "Airport & Commute" for the final leg

### Hotel Appointments
- Check-in: 3:00 PM on check-in date (hotel's timezone)
- Check-out: 12:00 PM on check-out date (hotel's timezone)
- Includes: confirmation number, address, phone, reservation details
- Set as "free" time
- Sage color (Google Calendar color code 6)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python travel_to_ics.py <pdf_file> [output_file]
```

Example:
```bash
python travel_to_ics.py my_trip.pdf my_trip.ics
```

## PDF Format Support

**This app is customized for CWT (Carlson Wagonlit Travel) itinerary PDFs.**

The parsing logic has been specifically tailored to work with CWT's Spanish-language itinerary format, which includes:

### Flight Information Extracted:
- Flight number (e.g., "LA 2696")
- Airport codes (3-letter IATA codes)
- Departure and arrival dates/times in Spanish format
- Reservation/PNR code (Localizador)
- Ticket number (Billete electrónico)

### Hotel Information Extracted:
- Hotel name
- Check-in/check-out dates (ENTRADA/SALIDA)
- Confirmation number (Confirmación de proveedor)
- Address (Dirección)
- Phone number (Teléfono)
- Room description

### Supported Airlines:
- LATAM Airlines
- LAN Airlines
- Avianca
- Sky Airlines
- Copa Airlines

If your travel agent uses a different PDF format, you'll need to adjust the regex patterns in the `parse_flights()` and `parse_hotels()` methods.

## Supported Airports

The app includes timezone mappings for major airports worldwide. If you need to add more airports, edit the `AIRPORT_TIMEZONES` dictionary in `travel_to_ics.py`.

## Importing to Google Calendar

1. Open Google Calendar
2. Click the "+" next to "Other calendars"
3. Select "Import"
4. Choose the generated .ics file
5. Select the destination calendar
6. Click "Import"

## Color Codes

- **Flamingo** (11): Flight and commute appointments
- **Sage** (6): Hotel stays

## Troubleshooting

### Parsing Issues
If the script doesn't extract information correctly:
1. Check the PDF text output
2. Update regex patterns in `parse_flights()` and `parse_hotels()`
3. Ensure date/time formats match your PDF

### Timezone Issues
If timezones are incorrect:
1. Verify airport codes are correct
2. Add missing airports to `AIRPORT_TIMEZONES` dictionary

### Import Issues
If Google Calendar doesn't accept the file:
1. Check that dates are valid
2. Ensure all required fields are present
3. Verify timezone names are valid

## License

MIT License - Feel free to modify and use as needed.

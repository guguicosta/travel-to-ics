#!/usr/bin/env python3
"""
Travel PDF to ICS Calendar Converter
Converts travel agent PDFs into Google Calendar ICS files with flight and hotel appointments.
"""

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from icalendar import Calendar, Event, Alarm
import PyPDF2
from pathlib import Path


# Airport timezone mapping (major airports)
AIRPORT_TIMEZONES = {
    'SCL': 'America/Santiago',
    'AEP': 'America/Argentina/Buenos_Aires',
    'EZE': 'America/Argentina/Buenos_Aires',
    'GRU': 'America/Sao_Paulo',
    'GIG': 'America/Sao_Paulo',
    'LIM': 'America/Lima',
    'BOG': 'America/Bogota',
    'MEX': 'America/Mexico_City',
    'MIA': 'America/New_York',
    'JFK': 'America/New_York',
    'LAX': 'America/Los_Angeles',
    'SFO': 'America/Los_Angeles',
    'ORD': 'America/Chicago',
    'DFW': 'America/Chicago',
    'ATL': 'America/New_York',
    'IAH': 'America/Chicago',
    'CDG': 'Europe/Paris',
    'LHR': 'Europe/London',
    'MAD': 'Europe/Madrid',
    'BCN': 'Europe/Madrid',
    'FCO': 'Europe/Rome',
    'AMS': 'Europe/Amsterdam',
    'FRA': 'Europe/Berlin',
    'MUC': 'Europe/Berlin',
    'ZRH': 'Europe/Zurich',
    'VIE': 'Europe/Vienna',
    'IST': 'Europe/Istanbul',
    'DXB': 'Asia/Dubai',
    'DOH': 'Asia/Qatar',
    'SIN': 'Asia/Singapore',
    'HKG': 'Asia/Hong_Kong',
    'NRT': 'Asia/Tokyo',
    'HND': 'Asia/Tokyo',
    'ICN': 'Asia/Seoul',
    'PEK': 'Asia/Shanghai',
    'PVG': 'Asia/Shanghai',
    'SYD': 'Australia/Sydney',
    'MEL': 'Australia/Melbourne',
    'AKL': 'Pacific/Auckland',
}


class FlightInfo:
    def __init__(self):
        self.flight_number = None
        self.origin = None
        self.destination = None
        self.departure_time = None
        self.arrival_time = None
        self.reservation_code = None
        self.ticket_number = None


class HotelInfo:
    def __init__(self):
        self.name = None
        self.checkin_date = None
        self.checkout_date = None
        self.confirmation_number = None
        self.address = None
        self.phone = None
        self.details = None
        self.timezone = None


class TravelPDFParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self._extract_text()

    def _extract_text(self):
        """Extract text from PDF file."""
        text = ""
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def _parse_spanish_date(self, date_str, time_str):
        """Parse Spanish date format like 'lu., mar. 23' with time '18:30'."""
        # Month mapping
        spanish_months = {
            'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
        }

        # Extract month and day from patterns like "lu., mar. 23" or "ma., mar. 24"
        match = re.search(r'[a-z]+\.,\s+([a-z]+)\.\s+(\d+)', date_str, re.IGNORECASE)
        if not match:
            return None

        month_abbr = match.group(1).lower()
        day = int(match.group(2))

        # Get year from text (look for pattern "mar. 23 - mar. 27, 2026")
        year_match = re.search(r',\s*(\d{4})', self.text)
        year = int(year_match.group(1)) if year_match else datetime.now().year

        month = spanish_months.get(month_abbr)
        if not month:
            return None

        # Parse time
        time_match = re.match(r'(\d{1,2}):(\d{2})', time_str)
        if not time_match:
            return None

        hour = int(time_match.group(1))
        minute = int(time_match.group(2))

        return datetime(year, month, day, hour, minute)

    def parse_flights(self):
        """Parse flight information from PDF text (CWT format)."""
        flights = []

        # Get the main booking reference (Localizador) from the top
        localizador_match = re.search(r'Localizador:\s*([A-Z0-9]+)', self.text)
        main_localizador = localizador_match.group(1) if localizador_match else None

        # Get the ticket number (Billete electrónico)
        ticket_match = re.search(r'Billete electrónico:\s*(\d+)', self.text)
        ticket_number = ticket_match.group(1) if ticket_match else None

        # In CWT format, flight details come BEFORE the airline/flight number line
        # Pattern: Flight details with SALIDA/LLEGADA, then "LAN AIRLINES LA 2696 CONFIRMADO"
        # We need to look backwards from the confirmation line

        # Find all "AIRLINE FLIGHTNO CONFIRMADO" lines
        confirmation_pattern = r'(?:LAN AIRLINES|LATAM AIRLINES|AVIANCA|SKY|COPA AIRLINES)\s+([A-Z]{2}\s*\d{3,4})\s+CONFIRMADO'
        confirmations = list(re.finditer(confirmation_pattern, self.text, re.IGNORECASE))

        for i, conf_match in enumerate(confirmations):
            flight = FlightInfo()
            flight.flight_number = conf_match.group(1).replace(' ', '')
            flight.reservation_code = main_localizador
            flight.ticket_number = ticket_number

            # Find the text BEFORE this confirmation (from previous confirmation or start)
            start_pos = confirmations[i-1].end() if i > 0 else 0
            end_pos = conf_match.start()
            flight_text = self.text[start_pos:end_pos]

            # Extract departure info: "lu., mar. 23 | 18:30"
            departure_match = re.search(r'SALIDA\s+([a-z]+\.,\s+[a-z]+\.\s+\d+)\s*\|\s*(\d{1,2}:\d{2})', flight_text, re.IGNORECASE)
            if departure_match:
                flight.departure_time = self._parse_spanish_date(departure_match.group(1), departure_match.group(2))

            # Extract arrival info: "lu., mar. 23 | 20:10"
            arrival_match = re.search(r'LLEGADA\s+([a-z]+\.,\s+[a-z]+\.\s+\d+)\s*\|\s*(\d{1,2}:\d{2})', flight_text, re.IGNORECASE)
            if arrival_match:
                flight.arrival_time = self._parse_spanish_date(arrival_match.group(1), arrival_match.group(2))

            # Extract origin airport from departure section
            origin_match = re.search(r'SALIDA.*?\n.*?\n.*?\(([A-Z]{3})\)', flight_text, re.DOTALL)
            if origin_match:
                flight.origin = origin_match.group(1)

            # Extract destination airport from arrival section
            dest_match = re.search(r'LLEGADA.*?\n.*?\n.*?\(([A-Z]{3})\)', flight_text, re.DOTALL)
            if dest_match:
                flight.destination = dest_match.group(1)

            # Validate we have all required info
            if all([flight.flight_number, flight.origin, flight.destination,
                   flight.departure_time, flight.arrival_time]):
                flights.append(flight)
                print(f"✓ Parsed flight: {flight.flight_number} {flight.origin} → {flight.destination}")
                print(f"  Departure: {flight.departure_time}")
                print(f"  Arrival: {flight.arrival_time}")
            else:
                print(f"⚠ Incomplete flight data for {flight.flight_number}")
                if not flight.departure_time:
                    print(f"  Missing: departure_time")
                if not flight.arrival_time:
                    print(f"  Missing: arrival_time")
                if not flight.origin:
                    print(f"  Missing: origin")
                if not flight.destination:
                    print(f"  Missing: destination")

        return flights

    def parse_hotels(self):
        """Parse hotel information from PDF text (CWT format)."""
        hotels = []

        # In CWT format, hotel dates (ENTRADA/SALIDA) come BEFORE the hotel name
        # Similar to flights
        # Pattern to find hotel confirmation lines
        hotel_pattern = r'(CASA ANDINA|NH COLLECTION|HOTEL|MARRIOTT|HILTON|HYATT|SHERATON|RADISSON|IBIS|HOLIDAY INN)([^\n]*?)\s+CONFIRMADO'

        hotel_matches = list(re.finditer(hotel_pattern, self.text, re.IGNORECASE))

        for i, match in enumerate(hotel_matches):
            hotel = HotelInfo()
            hotel.name = (match.group(1) + match.group(2)).strip()

            # Get text BEFORE this hotel name (from previous hotel or start of section)
            # and AFTER (for details)
            start_pos = hotel_matches[i-1].end() if i > 0 else 0
            end_pos = hotel_matches[i+1].start() if i < len(hotel_matches) - 1 else len(self.text)

            # Text before hotel name (for dates)
            before_text = self.text[start_pos:match.start()]
            # Text after hotel name (for details)
            after_text = self.text[match.end():end_pos]

            # Extract confirmation number
            conf_match = re.search(r'Confirmación de proveedor:\s*([A-Z0-9]+)', after_text)
            if conf_match:
                hotel.confirmation_number = conf_match.group(1)

            # Extract address
            address_match = re.search(r'Dirección:\s*([^\n]+)', after_text)
            if address_match:
                hotel.address = address_match.group(1).strip()

            # Extract phone
            phone_match = re.search(r'Teléfono:\s*([^\n]+)', after_text)
            if phone_match:
                hotel.phone = phone_match.group(1).strip()

            # Extract check-in date (ENTRADA) - look in text BEFORE hotel name
            # Pattern: "ENTRADA\nlu., mar. 23" (no time, just date on next line followed by newline)
            # This ensures we don't match flight dates which have " | HH:MM" after
            # Need to find the LAST occurrence (closest to hotel name)
            checkin_matches = list(re.finditer(r'ENTRADA\s*\n\s*([a-z]+\.,\s+[a-z]+\.\s+\d+)\s*\n', before_text, re.IGNORECASE))
            if checkin_matches:
                # Take the last match (closest to hotel name)
                checkin_date = self._parse_spanish_date(checkin_matches[-1].group(1), "15:00")
                if checkin_date:
                    hotel.checkin_date = checkin_date

            # Extract check-out date (SALIDA) - look in text BEFORE hotel name
            # Make sure it's a hotel SALIDA (no time) not a flight SALIDA (has time with |)
            # Pattern must have newline after date, not " | time"
            # Need to find the LAST occurrence (closest to hotel name) and ensure it's the hotel one
            salida_matches = list(re.finditer(r'SALIDA\s*\n\s*([a-z]+\.,\s+[a-z]+\.\s+\d+)\s*\n', before_text, re.IGNORECASE))
            if salida_matches:
                # Take the last match (closest to hotel name)
                checkout_date = self._parse_spanish_date(salida_matches[-1].group(1), "12:00")
                if checkout_date:
                    hotel.checkout_date = checkout_date

            # Extract room description for details
            room_desc_match = re.search(r'Descripción de la tarifa:\s*([^\n]+(?:\n(?!Notas:)[^\n]+)*)', after_text)
            if room_desc_match:
                hotel.details = room_desc_match.group(1).strip()

            # Determine timezone from city in address or hotel name
            if hotel.address:
                address_upper = hotel.address.upper()
                if 'LIMA' in address_upper or 'SAN ISIDRO' in address_upper or ', PE' in hotel.address:
                    hotel.timezone = 'America/Lima'
                elif 'BOGOTA' in address_upper or 'BOGOTÁ' in address_upper or ', CO' in hotel.address:
                    hotel.timezone = 'America/Bogota'
                elif 'SANTIAGO' in address_upper or ', CL' in hotel.address:
                    hotel.timezone = 'America/Santiago'
                elif 'BUENOS AIRES' in address_upper or ', AR' in hotel.address:
                    hotel.timezone = 'America/Argentina/Buenos_Aires'
                else:
                    hotel.timezone = 'UTC'
            else:
                hotel.timezone = 'UTC'

            # Validate we have required info
            if all([hotel.name, hotel.checkin_date, hotel.checkout_date, hotel.timezone]):
                hotels.append(hotel)
                print(f"✓ Parsed hotel: {hotel.name}")
                print(f"  Check-in: {hotel.checkin_date}")
                print(f"  Check-out: {hotel.checkout_date}")
                print(f"  Timezone: {hotel.timezone}")
            else:
                print(f"⚠ Incomplete hotel data for {hotel.name}")
                if not hotel.checkin_date:
                    print(f"  Missing: checkin_date")
                if not hotel.checkout_date:
                    print(f"  Missing: checkout_date")

        return hotels


class ICSGenerator:
    def __init__(self):
        self.calendar = Calendar()
        self.calendar.add('prodid', '-//Travel to ICS Converter//EN')
        self.calendar.add('version', '2.0')
        self.calendar.add('calscale', 'GREGORIAN')
        self.calendar.add('method', 'PUBLISH')

    def get_timezone(self, airport_code):
        """Get timezone for airport code."""
        return AIRPORT_TIMEZONES.get(airport_code, 'UTC')

    def get_commute_duration(self, airport_code, is_departure=True):
        """Get commute duration based on airport and direction."""
        if is_departure:
            # Before flight: 2.5 hours for SCL, 3.5 for others
            return timedelta(hours=2.5) if airport_code == 'SCL' else timedelta(hours=3.5)
        else:
            # After landing: 1 hour for AEP/SCL, 1.5 for others
            return timedelta(hours=1) if airport_code in ['AEP', 'SCL'] else timedelta(hours=1.5)

    def add_flight_event(self, flight):
        """Add flight event with proper timezones."""
        event = Event()

        # Title with flight number and airports
        event.add('summary', f'Flight {flight.flight_number}: {flight.origin} → {flight.destination}')

        # Description with reservation and ticket info
        description = f'Reservation Code: {flight.reservation_code}\n'
        if flight.ticket_number:
            description += f'Ticket Number: {flight.ticket_number}'
        event.add('description', description)

        # Start and end times with proper timezones
        origin_tz = ZoneInfo(self.get_timezone(flight.origin))
        dest_tz = ZoneInfo(self.get_timezone(flight.destination))

        dtstart = flight.departure_time.replace(tzinfo=origin_tz)
        dtend = flight.arrival_time.replace(tzinfo=dest_tz)

        event.add('dtstart', dtstart)
        event.add('dtend', dtend)

        # Color (flamingo = 11 in Google Calendar)
        event.add('color', '11')

        # Status
        event.add('status', 'CONFIRMED')
        event.add('transp', 'OPAQUE')  # Show as busy

        # 48-hour alarm
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('trigger', timedelta(hours=-48))
        alarm.add('description', f'Flight {flight.flight_number} in 48 hours')
        event.add_component(alarm)

        self.calendar.add_component(event)
        return event

    def add_commute_event(self, title, start_time, end_time, timezone_str, description=''):
        """Add commute event (before or after flight)."""
        event = Event()
        event.add('summary', title)

        if description:
            event.add('description', description)

        # Use the provided timezone
        tz = ZoneInfo(timezone_str)
        dtstart = start_time.replace(tzinfo=tz)
        dtend = end_time.replace(tzinfo=tz)

        event.add('dtstart', dtstart)
        event.add('dtend', dtend)

        # Color (flamingo = 11)
        event.add('color', '11')

        # Status
        event.add('status', 'CONFIRMED')
        event.add('transp', 'OPAQUE')  # Show as busy

        self.calendar.add_component(event)
        return event

    def add_hotel_event(self, hotel):
        """Add hotel event."""
        event = Event()

        # Title with hotel name
        event.add('summary', hotel.name)

        # Description with all details
        description = []
        if hotel.confirmation_number:
            description.append(f'Confirmation: {hotel.confirmation_number}')
        if hotel.address:
            description.append(f'Address: {hotel.address}')
        if hotel.phone:
            description.append(f'Phone: {hotel.phone}')
        if hotel.details:
            description.append(f'Details: {hotel.details}')

        event.add('description', '\n'.join(description))

        # Set timezone for hotel location
        tz = ZoneInfo(hotel.timezone)

        # Check-in: 3:00 PM on check-in date
        checkin = hotel.checkin_date.replace(hour=15, minute=0, second=0, microsecond=0, tzinfo=tz)
        # Check-out: 12:00 PM on check-out date
        checkout = hotel.checkout_date.replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=tz)

        event.add('dtstart', checkin)
        event.add('dtend', checkout)

        # Color (sage = 6 in Google Calendar)
        event.add('color', '6')

        # Status
        event.add('status', 'CONFIRMED')
        event.add('transp', 'TRANSPARENT')  # Show as free

        self.calendar.add_component(event)
        return event

    def process_flights(self, flights):
        """Process all flights and add events with commute times."""
        if not flights:
            return

        # Sort flights by departure time
        flights.sort(key=lambda f: f.departure_time)

        for i, flight in enumerate(flights):
            # Check if this is a connecting flight
            is_first_leg = (i == 0)
            is_last_leg = (i == len(flights) - 1)

            is_connection = False
            if not is_last_leg:
                next_flight = flights[i + 1]
                # Check if connection (same airport, less than 12 hours)
                if (flight.destination == next_flight.origin and
                    (next_flight.departure_time - flight.arrival_time) < timedelta(hours=12)):
                    is_connection = True

            # Add "commute & airport" before flight (only if first leg or not a connection)
            if is_first_leg or not is_connection:
                origin_tz = self.get_timezone(flight.origin)
                commute_duration = self.get_commute_duration(flight.origin, is_departure=True)
                commute_start = flight.departure_time - commute_duration

                self.add_commute_event(
                    'Commute & Airport',
                    commute_start,
                    flight.departure_time,
                    origin_tz,
                    f'Travel to {flight.origin} for flight {flight.flight_number}'
                )

            # Add flight event
            self.add_flight_event(flight)

            # Add "airport & commute" after flight (only if last leg or not connecting)
            was_connection_from_previous = False
            if not is_first_leg:
                prev_flight = flights[i - 1]
                if (prev_flight.destination == flight.origin and
                    (flight.departure_time - prev_flight.arrival_time) < timedelta(hours=12)):
                    was_connection_from_previous = True

            if is_last_leg or not was_connection_from_previous:
                dest_tz = self.get_timezone(flight.destination)
                commute_duration = self.get_commute_duration(flight.destination, is_departure=False)
                commute_end = flight.arrival_time + commute_duration

                self.add_commute_event(
                    'Airport & Commute',
                    flight.arrival_time,
                    commute_end,
                    dest_tz,
                    f'Travel from {flight.destination} after flight {flight.flight_number}'
                )

    def save(self, output_path):
        """Save calendar to ICS file."""
        with open(output_path, 'wb') as f:
            f.write(self.calendar.to_ical())


def main():
    """Main function to convert PDF to ICS."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python travel_to_ics.py <pdf_file> [output_file]")
        print("\nThis script converts travel agent PDFs to ICS calendar files.")
        print("\nNote: The PDF parsing logic needs to be customized based on")
        print("your specific travel agent's PDF format. Please provide a sample")
        print("PDF so the parsing patterns can be adjusted accordingly.")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'travel_calendar.ics'

    # Parse PDF
    print(f"Parsing PDF: {pdf_path}")
    parser = TravelPDFParser(pdf_path)
    flights = parser.parse_flights()
    hotels = parser.parse_hotels()

    # Generate ICS
    print(f"\nGenerating ICS file: {output_path}")
    generator = ICSGenerator()

    # Add flights with commute events
    generator.process_flights(flights)

    # Add hotel events
    for hotel in hotels:
        generator.add_hotel_event(hotel)

    # Save to file
    generator.save(output_path)
    print(f"\n✓ Calendar file created: {output_path}")
    print(f"  - {len(flights)} flights processed")
    print(f"  - {len(hotels)} hotels processed")
    print(f"\nYou can now import this file into Google Calendar.")


if __name__ == '__main__':
    main()

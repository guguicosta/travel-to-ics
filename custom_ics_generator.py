"""
Custom ICS Generator with configurable colors and commute times
"""

from datetime import timedelta
from travel_to_ics import ICSGenerator as BaseICSGenerator, FlightInfo, HotelInfo


# Google Calendar color mapping
COLOR_MAP = {
    '1': '#A4BDFC',   # Lavender
    '2': '#7AE7BF',   # Sage
    '3': '#DBADFF',   # Grape
    '4': '#FF887C',   # Flamingo/Blossom
    '5': '#FBD75B',   # Banana
    '6': '#0B8043',   # Basil/Sage (green)
    '7': '#46D6DB',   # Peacock
    '8': '#E1E1E1',   # Graphite
    '9': '#5484ED',   # Blueberry
    '10': '#FF6C00',  # Tangerine
    '11': '#F6BF26',  # Flamingo (orange/pink)
}


class CustomICSGenerator(BaseICSGenerator):
    """ICS Generator with custom color and commute time settings"""

    def __init__(self, flight_color='11', hotel_color='6', airport_times=None):
        """
        Initialize generator with custom settings

        Args:
            flight_color: Google Calendar color ID for flights (1-11)
            hotel_color: Google Calendar color ID for hotels (1-11)
            airport_times: Dict of airport codes to commute times
                          Format: {
                              'SCL_before': 2.5, 'SCL_after': 1.0,
                              'AEP_before': 3.5, 'AEP_after': 1.0,
                              ...
                          }
        """
        super().__init__()
        self.flight_color = str(flight_color)
        self.hotel_color = str(hotel_color)
        self.airport_times = airport_times or {}

    def _prepare_flights_with_commutes(self, flights):
        """
        Prepare flight data with commute information for Google Calendar API.

        Args:
            flights: List of FlightInfo objects

        Returns:
            List of dicts with flight and commute information
        """
        from travel_to_ics import AIRPORT_TIMEZONES

        processed_flights = []

        for i, flight in enumerate(flights):
            flight_data = {'flight': flight}

            # Check if we need commute before (first flight or connection break)
            needs_commute_before = True
            if i > 0:
                prev_flight = flights[i - 1]
                time_diff = (flight.departure_time - prev_flight.arrival_time).total_seconds() / 3600
                if time_diff < 12 and flight.origin == prev_flight.destination:
                    needs_commute_before = False

            # Check if we need commute after (last flight or connection break)
            needs_commute_after = True
            if i < len(flights) - 1:
                next_flight = flights[i + 1]
                time_diff = (next_flight.departure_time - flight.arrival_time).total_seconds() / 3600
                if time_diff < 12 and flight.destination == next_flight.origin:
                    needs_commute_after = False

            # Add commute before if needed
            if needs_commute_before:
                commute_duration = self.get_commute_duration(flight.origin, is_departure=True)
                origin_tz = AIRPORT_TIMEZONES.get(flight.origin, 'UTC')

                flight_data['commute_before'] = {
                    'title': f'Commute to {flight.origin} Airport',
                    'start': flight.departure_time - commute_duration,
                    'end': flight.departure_time,
                    'timezone': origin_tz,
                    'description': f'Travel to airport for flight {flight.flight_number}'
                }

            # Add commute after if needed
            if needs_commute_after:
                commute_duration = self.get_commute_duration(flight.destination, is_departure=False)
                dest_tz = AIRPORT_TIMEZONES.get(flight.destination, 'UTC')

                flight_data['commute_after'] = {
                    'title': f'Commute from {flight.destination} Airport',
                    'start': flight.arrival_time,
                    'end': flight.arrival_time + commute_duration,
                    'timezone': dest_tz,
                    'description': f'Travel from airport after flight {flight.flight_number}'
                }

            processed_flights.append(flight_data)

        return processed_flights

    def get_commute_duration(self, airport_code, is_departure=True):
        """
        Get commute duration based on airport and direction.
        Uses custom settings if provided, otherwise falls back to defaults.
        """
        direction = 'before' if is_departure else 'after'
        key = f'{airport_code}_{direction}'

        # Check if custom time is set for this specific airport
        if key in self.airport_times:
            return timedelta(hours=float(self.airport_times[key]))

        # Check for international default
        if f'international_{direction}' in self.airport_times:
            # Use international default for non-specified airports
            if airport_code not in ['SCL', 'AEP', 'EZE', 'GRU', 'MEX']:
                return timedelta(hours=float(self.airport_times[f'international_{direction}']))

        # Fall back to original defaults
        return super().get_commute_duration(airport_code, is_departure)

    def add_flight_event(self, flight):
        """Add flight event with custom color"""
        event = super().add_flight_event(flight)

        # Update color properties (use both add() and direct assignment for compatibility)
        color_rgb = COLOR_MAP.get(self.flight_color, COLOR_MAP['11'])

        # Remove old color properties
        if 'color' in event:
            del event['color']
        if 'COLOR' in event:
            del event['COLOR']
        if 'x-google-calendar-content-color' in event:
            del event['x-google-calendar-content-color']
        if 'x-google-calendar-event-color' in event:
            del event['x-google-calendar-event-color']

        # Add new color properties
        event.add('color', self.flight_color)
        event['COLOR'] = self.flight_color
        event.add('x-google-calendar-content-color', color_rgb)
        event.add('x-google-calendar-event-color', self.flight_color)

        return event

    def add_commute_event(self, title, start_time, end_time, timezone_str, description=''):
        """Add commute event with custom color"""
        event = super().add_commute_event(title, start_time, end_time, timezone_str, description)

        # Update color properties (use both add() and direct assignment for compatibility)
        color_rgb = COLOR_MAP.get(self.flight_color, COLOR_MAP['11'])

        # Remove old color properties
        if 'color' in event:
            del event['color']
        if 'COLOR' in event:
            del event['COLOR']
        if 'x-google-calendar-content-color' in event:
            del event['x-google-calendar-content-color']
        if 'x-google-calendar-event-color' in event:
            del event['x-google-calendar-event-color']

        # Add new color properties
        event.add('color', self.flight_color)
        event['COLOR'] = self.flight_color
        event.add('x-google-calendar-content-color', color_rgb)
        event.add('x-google-calendar-event-color', self.flight_color)

        # Ensure it's marked as BUSY
        if 'transp' in event:
            del event['transp']
        event.add('transp', 'OPAQUE')

        return event

    def add_hotel_event(self, hotel):
        """Add hotel event with custom color"""
        event = super().add_hotel_event(hotel)

        # Update color properties (use both add() and direct assignment for compatibility)
        color_rgb = COLOR_MAP.get(self.hotel_color, COLOR_MAP['6'])

        # Remove old color properties
        if 'color' in event:
            del event['color']
        if 'COLOR' in event:
            del event['COLOR']
        if 'x-google-calendar-content-color' in event:
            del event['x-google-calendar-content-color']
        if 'x-google-calendar-event-color' in event:
            del event['x-google-calendar-event-color']

        # Add new color properties
        event.add('color', self.hotel_color)
        event['COLOR'] = self.hotel_color
        event.add('x-google-calendar-content-color', color_rgb)
        event.add('x-google-calendar-event-color', self.hotel_color)

        # Ensure it's marked as FREE (TRANSPARENT)
        if 'transp' in event:
            del event['transp']
        event.add('transp', 'TRANSPARENT')

        return event

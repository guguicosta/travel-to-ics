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

        # Update color
        color_rgb = COLOR_MAP.get(self.flight_color, COLOR_MAP['11'])
        event['COLOR'] = self.flight_color
        event['X-GOOGLE-CALENDAR-CONTENT-COLOR'] = color_rgb
        event['X-GOOGLE-CALENDAR-EVENT-COLOR'] = self.flight_color

        return event

    def add_commute_event(self, title, start_time, end_time, timezone_str, description=''):
        """Add commute event with custom color"""
        event = super().add_commute_event(title, start_time, end_time, timezone_str, description)

        # Update color
        color_rgb = COLOR_MAP.get(self.flight_color, COLOR_MAP['11'])
        event['COLOR'] = self.flight_color
        event['X-GOOGLE-CALENDAR-CONTENT-COLOR'] = color_rgb
        event['X-GOOGLE-CALENDAR-EVENT-COLOR'] = self.flight_color

        return event

    def add_hotel_event(self, hotel):
        """Add hotel event with custom color"""
        event = super().add_hotel_event(hotel)

        # Update color
        color_rgb = COLOR_MAP.get(self.hotel_color, COLOR_MAP['6'])
        event['COLOR'] = self.hotel_color
        event['X-GOOGLE-CALENDAR-CONTENT-COLOR'] = color_rgb
        event['X-GOOGLE-CALENDAR-EVENT-COLOR'] = self.hotel_color

        return event

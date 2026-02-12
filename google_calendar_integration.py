"""
Google Calendar API Integration
Allows direct push of events to Google Calendar
"""

import os
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendarIntegration:
    """Handle Google Calendar API operations"""

    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        """
        Initialize Google Calendar integration

        Args:
            credentials_file: Path to OAuth2 credentials JSON file
            token_file: Path to save/load user tokens
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.service = None

        # Check if credentials file exists
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(
                f"Google Calendar credentials not configured.\n"
                f"Please follow GOOGLE_CALENDAR_SETUP.md to create {self.credentials_file}"
            )

    def get_authorization_url(self, redirect_uri):
        """
        Get the authorization URL for OAuth2 flow

        Args:
            redirect_uri: Callback URL after authorization

        Returns:
            tuple: (authorization_url, state)
        """
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.SCOPES,
            redirect_uri=redirect_uri
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        return authorization_url, state

    def handle_oauth_callback(self, authorization_response, state, redirect_uri):
        """
        Handle the OAuth2 callback and exchange code for tokens

        Args:
            authorization_response: Full callback URL with code
            state: State parameter from initial request
            redirect_uri: Callback URL

        Returns:
            bool: True if successful
        """
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.SCOPES,
            state=state,
            redirect_uri=redirect_uri
        )

        flow.fetch_token(authorization_response=authorization_response)

        self.creds = flow.credentials

        # Save credentials for future use
        with open(self.token_file, 'wb') as token:
            pickle.dump(self.creds, token)

        return True

    def load_credentials(self):
        """
        Load saved credentials or refresh if expired

        Returns:
            bool: True if credentials are valid
        """
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)

        # Refresh credentials if expired
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)

        if self.creds and self.creds.valid:
            self.service = build('calendar', 'v3', credentials=self.creds)
            return True

        return False

    def create_event(self, summary, start_datetime, end_datetime,
                    description='', location='', timezone='UTC',
                    color_id=None, reminders=None, transparency='opaque'):
        """
        Create a single calendar event

        Args:
            summary: Event title
            start_datetime: Start datetime object
            end_datetime: End datetime object
            description: Event description
            location: Event location
            timezone: Timezone string (e.g., 'America/Santiago')
            color_id: Google Calendar color ID (1-11)
            reminders: List of reminders in minutes (e.g., [10, 2880])
            transparency: 'opaque' (busy) or 'transparent' (free)

        Returns:
            dict: Created event data
        """
        if not self.service:
            if not self.load_credentials():
                raise Exception("Not authenticated with Google Calendar")

        # Format datetime for Google Calendar API
        start_tz = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        end_tz = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_tz,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_tz,
                'timeZone': timezone,
            },
            'transparency': transparency,
        }

        if location:
            event['location'] = location

        if color_id:
            event['colorId'] = str(color_id)

        if reminders:
            event['reminders'] = {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': minutes} for minutes in reminders
                ]
            }

        try:
            event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()

            return event

        except HttpError as error:
            print(f'An error occurred: {error}')
            raise

    def create_flight_event(self, flight, color_id='11'):
        """
        Create a flight event with 48-hour reminder

        Args:
            flight: FlightInfo object
            color_id: Google Calendar color ID

        Returns:
            dict: Created event data
        """
        summary = f"Flight {flight.flight_number}: {flight.origin} → {flight.destination}"
        description = f"Reservation Code: {flight.reservation_code}\n"
        if flight.ticket_number:
            description += f"Ticket Number: {flight.ticket_number}"

        # Get timezone for departure
        from travel_to_ics import AIRPORT_TIMEZONES
        origin_tz = AIRPORT_TIMEZONES.get(flight.origin, 'UTC')

        return self.create_event(
            summary=summary,
            start_datetime=flight.departure_time,
            end_datetime=flight.arrival_time,
            description=description,
            timezone=origin_tz,
            color_id=color_id,
            reminders=[2880],  # 48 hours in minutes
            transparency='opaque'
        )

    def create_hotel_event(self, hotel, color_id='6'):
        """
        Create a hotel event

        Args:
            hotel: HotelInfo object
            color_id: Google Calendar color ID

        Returns:
            dict: Created event data
        """
        summary = hotel.name

        description_parts = []
        if hotel.confirmation_number:
            description_parts.append(f"Confirmation: {hotel.confirmation_number}")
        if hotel.address:
            description_parts.append(f"Address: {hotel.address}")
        if hotel.phone:
            description_parts.append(f"Phone: {hotel.phone}")
        if hotel.details:
            description_parts.append(f"Details: {hotel.details}")

        description = '\n'.join(description_parts)

        return self.create_event(
            summary=summary,
            start_datetime=hotel.checkin_date,
            end_datetime=hotel.checkout_date,
            description=description,
            location=hotel.address or '',
            timezone=hotel.timezone,
            color_id=color_id,
            transparency='transparent'  # Show as free
        )

    def create_commute_event(self, title, start_datetime, end_datetime,
                            timezone, description='', color_id='11'):
        """
        Create a commute event

        Args:
            title: Event title
            start_datetime: Start datetime
            end_datetime: End datetime
            timezone: Timezone string
            description: Event description
            color_id: Google Calendar color ID

        Returns:
            dict: Created event data
        """
        return self.create_event(
            summary=title,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            description=description,
            timezone=timezone,
            color_id=color_id,
            transparency='opaque'
        )

    def batch_create_events(self, events_data):
        """
        Create multiple events at once

        Args:
            events_data: List of event dictionaries

        Returns:
            list: Created events
        """
        created_events = []

        for event_data in events_data:
            try:
                created_event = self.create_event(**event_data)
                created_events.append(created_event)
            except Exception as e:
                print(f"Error creating event {event_data.get('summary')}: {e}")

        return created_events

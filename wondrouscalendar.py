# Import the components needed to conjure the power of Google Calendar API
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope and the file path to the service account credentials
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "/Users/jamalelakrah/Documents/GitHub/MMMSS/omnibud-axhq-753417b9cb96.json"

# Create the credentials object from the service account file and the defined scope
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build the Google Calendar API client
calendar_api = build("calendar", "v3", credentials=credentials)

# Define a function to create an event in the Google Calendar
def create_event():
    try:
        # Define the event object with its properties
        event_object = {
            'summary': 'Appointment',
            'location': 'Somewhere',
            'start': {
                'dateTime': '2023-04-21T10:00:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2023-04-21T11:00:00',
                'timeZone': 'America/Los_Angeles',
            },
        }

        # Insert the event into the primary calendar and execute the request
        created_event = calendar_api.events().insert(calendarId="primary", body=event_object).execute()

        # Print the created event's link
        print(f'Event created: {created_event.get("htmlLink")}')
    except HttpError as error:
        # Handle any errors that occur during the event creation
        print(f"An error occurred: {error}")
        created_event = None
    return created_event

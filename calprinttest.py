import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import arrow

from Adafruit_Thermal import *


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """
    Creates a Google Calendar API service object and outputs a list of the events on the user's calendar that take place today.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #Get dates in RFC3339 timestamp format
    today = str(datetime.datetime.now().date()) + "T00:00:00.00Z"
    tommorow = str(datetime.datetime.now().date()+ datetime.timedelta(days=3) ) + "T00:00:00.00Z"

    eventsResult = service.events().list(
        calendarId='primary', timeMin=today, timeMax=tommorow, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    printer.doubleHeightOn()
    printer.println(arrow.utcnow().format('dddd, MMMM DD, YYYY'))
    printer.doubleHeightOff()

    if not events:
        print('No events today.')
    for event in events:
        printer.boldOn()
        printer.underlineOn(2)
        printer.println(event['summary'])
        printer.boldOff()
        printer.underlineOff()

        start = arrow.get(event['start'].get('dateTime', event['start'].get('date')))
        printer.println(start.format('h:mm A'))

        # for attendee in event['attendees']:
        #     if attendee['responseStatus'] == "accepted":
        #         if 'displayName' in attendee:
        #             printer.println(attendee['displayName'])
        #         elif 'email' in attendee:
        #             printer.println(attendee['email'])

        printer.println()

if __name__ == '__main__':
    main()

    printer.sleep()      # Tell printer to sleep
    printer.wake()       # Call wake() before printing again, even if reset
    printer.setDefault() # Restore printer to defaults
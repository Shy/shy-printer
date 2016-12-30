import time, schedule

import httplib2
import os
import textwrap

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
    printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)
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

def printcal():
    printer.println()

    """
    Creates a Google Calendar API service object and outputs a list of the events on the user's calendar that take place today.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #Hardcoded dates for testing
    today = '2016-11-23T00:00:00+00:00'
    tommorow = "2016-11-24T00:00:00+00:00"

    #Get dates in RFC3339 timestamp format
    # today = str(datetime.datetime.now().date()) + "T00:00:00.00Z"
    # tommorow = str(datetime.datetime.now().date()+ datetime.timedelta(days=1) ) + "T00:00:00.00Z"

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

        #Truncate out details that I'm attending the meeting to save width.
        event_name = event['summary']
        if " <> Shy (Major League Hacking)" in event_name:
            event_name = event_name[:event_name.index(" <> Shy")]
        event_name = textwrap.wrap(event_name,32)

        printer.boldOn()
        printer.underlineOn(2)

        for line in event_name:
            printer.println(line)

        printer.boldOff()
        printer.underlineOff()

        start = arrow.get(event['start'].get('dateTime', event['start'].get('date')))
        end = arrow.get(event['end'].get('dateTime', event['end'].get('date')))
        printer.println('{} - {}'.format(start.format('h:mm A'),end.format('h:mm A')))

        # for attendee in event['attendees']:
        #     if attendee['responseStatus'] == "accepted":
        #         if 'displayName' in attendee:
        #             printer.println(attendee['displayName'])
        #         elif 'email' in attendee:
        #             printer.println(attendee['email'])

        printer.println()

def main():
    schedule.every().day.at("19:41").do(printcal)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()

    printer.println()
    printer.sleep()      # Tell printer to sleep
    printer.wake()       # Call wake() before printing again, even if reset
    printer.setDefault() # Restore printer to defaults
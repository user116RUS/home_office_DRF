from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    calendarWorkTime = []

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/ramilnurgaleev/PycharmProjects/homme_office_bot/bot/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        """now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='homeoffice.nch@gmail.com', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])"""

        # Перебор календарей
        page_token = None

        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                # Call the Calendar API
                calendarWorkTime.append(calendar_list_entry["summary"])
                calendarWorkTime.append('занято :')
                now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
                print(f'\n\nМероприятия из \'{calendar_list_entry["summary"]}\':')
                events_result = service.events().list(calendarId=calendar_list_entry['id'], timeMin=now,
                                                      maxResults=10, singleEvents=True,
                                                      orderBy='startTime').execute()
                events = events_result.get('items', [])

                if not events:
                    print('Мероприятия не запланированы')

                # Prints the start and name of the next 10 events
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    end = event['end'].get('dateTime')
                    calendarWorkTime.append('от')
                    calendarWorkTime.append(start)
                    if end:
                        calendarWorkTime.append('до')
                        calendarWorkTime.append(end)
                    calendarWorkTime.append('и')
                    print(start, event['summary'])
                    print(end)
                if calendarWorkTime[-1] != ':':
                    calendarWorkTime.append('.\n')
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        print("\n\n" + ' '.join(calendarWorkTime))
        return calendarWorkTime

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()

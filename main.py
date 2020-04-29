from __future__ import print_function
import csv
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_data():
    total = []

    with open('Untitled Database.csv', 'r') as data:
        csv_reader = csv.reader(data, delimiter=',')
        line_count = 0
        data = []
        for row in csv_reader:
            if line_count == 0:
                print(f'column names are {",".join(row)}')
                line_count += 1
            else:
                date = row[0].split("-")
                time = row[4].split(":")

                x = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]),
                                      int(time[2]))
                x = x + datetime.timedelta(days=+1)
                y = x + datetime.timedelta(minutes=-30)
                summary = "Hand in " + row[1]
                description = row[2]
                values = (y, x, summary, description)
                data.append(values)
                line_count += 1
        return data


def main():
    # this shows the basic usage of the google calendar api
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events',
              'https://www.googleapis.com/auth/calendar.events.readonly',
              'https://www.googleapis.com/auth/calendar.readonly',
              'https://www.googleapis.com/auth/calendar.settings.readonly']
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there is no (valid crdential availivble let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # call the calendar api
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    # value for the time zone
    GMT_OFF = '+02:00'
    # Get the data from the .csv file
    data = get_data()

    # Loop through the data tuples
    for item in data:
        # Get the data form the tuples to correct format for the api
        start_time = str(item[0]) + "%s" % GMT_OFF
        start_time = start_time.replace(" ", "T")
        end_time = str(item[1]) + "%s" % GMT_OFF
        end_time = end_time.replace(" ", "T")
        summary = item[2]
        description = "subject(s): " + item[3]

        EVENT = {
            'summary': summary,
            'start': {'dateTime': start_time},
            'end': {'dateTime': end_time},
            'description': description
        }

        e = service.events().insert(calendarId='primary',
                                    body=EVENT).execute()

        print(get_data())
        print(''' *** %r event added
                Start: %s
                End: %s''' % (e['summary'].encode('utf-8'),
                              e['start']['dateTime'], e['end']['dateTime']))

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()

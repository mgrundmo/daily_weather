import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly"]

def calendar():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming event")
    events_result = (
        service.events()
        .list(
            calendarId="sgmatnnlv1bv86k34qk0keri1t2chq94@import.calendar.google.com",
            timeMin=now,
            maxResults=1,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      wann_spielt_fc = "Erstmal nicht"
      return wann_spielt_fc

    # Prints the start and name of the next event
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      year = start[:4]
      month = start[5:-18]
      day = start[8:-15]
      hour = start[11:-12]
      minute = start[14:-9]
      new_start = day + '.' + month + '.' + year + '  ' + hour + ':' + minute
      wann_spielt_fc = new_start + '    ' + event["summary"]
      return wann_spielt_fc

  except HttpError as error:
    print(f"An error occurred: {error}")

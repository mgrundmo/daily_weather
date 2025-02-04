import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly"]

def calendar(detailed_cal):
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

  #getting info from FC Calendar
  try:
    service = build("calendar", "v3", credentials=creds)
    
    # Call the FC Calendar API
    id = "sgmatnnlv1bv86k34qk0keri1t2chq94@import.calendar.google.com"
    results = 1   
    wann_spielt_fc_list = cal(service, id, results)
    #store list item in single variable
    wann_spielt_fc = wann_spielt_fc_list.pop(0)

    # call personal calendar    
    my_cal = []
    if detailed_cal == True:
      id = "primary"
      results = 5
      my_cal = cal(service, id, results)
    return wann_spielt_fc, my_cal

  except HttpError as error:
    print(f"An error occurred: {error}")

def cal(service, id, results):
  now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
  events_result = (
      service.events()
      .list(
        calendarId=id,
        timeMin=now,
        maxResults=results,
        singleEvents=True,
        orderBy="startTime",
      )
      .execute()
  )
  events = events_result.get("items", [])
  cal_list =[]  
  if not events:
    print("No upcoming events found.")
    cal_entry = "Erstmal nicht"
    return cal_entry

    # Prints the start and name of the next event
  for event in events:
    start = event["start"].get("dateTime", event["start"].get("date"))
    year = start[:4]
    month = start[5:-18]
    day = start[8:-15]
    hour = start[11:-12]
    minute = start[14:-9]
    new_start = day + '.' + month + '.' + year + '  ' + hour + ':' + minute
    cal_entry = new_start + '    ' + event["summary"]
    cal_list.append(cal_entry)
  return cal_list
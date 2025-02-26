import os
import smtplib

from datetime import date
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from helpers import forecast_weather, moon, email_text, email_html, aqi, last_fc, useless_facts, jacquie_jokes

load_dotenv()

#sender email
email = os.environ.get('MAILUSER')
password = os.environ.get('PASSWORD')

# list of adresses
adresses = [
    {'email': os.environ.get('EMAIL1'), 'lat': os.environ.get('LAT1'), 'lng': os.environ.get('LNG1')},
    {'email': os.environ.get('EMAIL2'), 'lat': os.environ.get('LAT2'), 'lng': os.environ.get('LNG2')},
    {'email': os.environ.get('EMAIL3'), 'lat': os.environ.get('LAT3'), 'lng': os.environ.get('LNG3')},
    {'email': os.environ.get('EMAIL4'), 'lat': os.environ.get('LAT4'), 'lng': os.environ.get('LNG4')},
    {'email': os.environ.get('EMAIL5'), 'lat': os.environ.get('LAT5'), 'lng': os.environ.get('LNG5')}
]

#getting todays date and weekday
today = date.today()
weekday = today.strftime("%A, %d %B %Y")

#getting result of last FC match
last_match_fc, next_match_fc = last_fc()

#getting useless facts
uselessfacts = useless_facts()
random_joke = jacquie_jokes()

for adresse in adresses:
    for i in range(0, len(adresse), 4):
        receiver_email = adresse['email']
        #preparing geo data for weather api and request data
        geo_location = str(adresse['lat']) + "," + str(adresse['lng'])
        weather = forecast_weather(geo_location)      
        moon_phase_de = moon(weather['moon_phase'])

        #getting information of next FC match and personal calender if "detailed_cal = True"  
        #detailed_cal = adresse['detailed_cal']         
        #wann_spielt_fc, my_cal = calendar(detailed_cal)

        #preparing geo data for AQI request and get data
        lat = adresse['lat']
        lng = adresse['lng']
        aqi_data = aqi(lat, lng)
        
        #prepare emails
        #plain text email as backup
        text = email_text(weather, weekday, aqi_data, next_match_fc, last_match_fc, uselessfacts, random_joke)
        print(text)

        #html email as primary
        html = email_html(weather, weekday, aqi_data, next_match_fc, last_match_fc, uselessfacts, random_joke)

        #creating header of email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Das Wetter für " +str(weather['location']) +" am " +str(weekday)
        msg['From'] = email
        msg['To'] = receiver_email

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)
        #'''
        #sending email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, receiver_email, msg.as_string())
        print("Email has been sent to " + receiver_email + "\n")
server.quit()
#'''
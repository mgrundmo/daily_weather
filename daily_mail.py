import smtplib

from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from helpers import forecast_weather, moon, email_text, email_html, aqi, last_fc, useless_facts
from quickstart import calendar

#sender email
email = "mgrundmo@gmail.com"

# list of adresses
adresses = [
    {'email': 'mgrundmo@gmx.de', 'lat': 50.891120, 'lng': 6.910415, 'detailed_cal': True},
    {'email': 'sissi-michael@gmx.de', 'lat': 43.542287, 'lng': 4.131755, 'detailed_cal': False},
    {'email': 'philippcolonia@gmail.com', 'lat': 13.713353, 'lng': 100.505084, 'detailed_cal': False},
    {'email': 'cedric.riechers@web.de','lat': 50.868795, 'lng': 7.004098, 'detailed_cal': False}
]

#getting todays date and weekday
today = date.today()
weekday = today.strftime("%A, %d %B %Y")

#getting result of last FC match
last_match_fc, next_match_fc = last_fc()

#getting useless facts
uselessfacts = useless_facts()

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
        text = email_text(weather, weekday, aqi_data, next_match_fc, last_match_fc, uselessfacts)
        print(text)

        #html email as primary
        html = email_html(weather, weekday, aqi_data, next_match_fc, last_match_fc, uselessfacts)

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
        server.login(email, "xmtnrolasszlaihl")
        server.sendmail(email, receiver_email, msg.as_string())
        print("Email has been sent to " + receiver_email + "\n")
server.quit()
#'''
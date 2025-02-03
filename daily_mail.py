import smtplib

from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from helpers import forecast_weather, moon, email_text, email_html, aqi, last_fc, useless_facts
from quickstart import calendar

email = "mgrundmo@gmail.com"

# list of adresses
adresses = [
    {'email': 'mgrundmo@gmx.de','location': 'Hürth', 'detailed_cal': True},
   # {'email': 'philippcolonia@gmail.com', 'location': 'Bangkok', 'detailed_cal': False},
   # {'email': 'cedric.riechers@web.de','location': 'Cologne', 'detailed_cal': False}
]

#getting todays date and weekday
today = date.today()
weekday = today.strftime("%A, %d %B %Y")

#getting result of last FC match
last_match_fc = last_fc()

#getting useless facts
uselessfacts = useless_facts()

for adresse in adresses:
    for i in range(0, len(adresse), 3):
        receiver_email = adresse['email']
        location = adresse['location']
        detailed_cal = adresse['detailed_cal']
        #getting information of next FC match and personal calender if "detailed_cal = True"      
        wann_spielt_fc, my_cal = calendar(detailed_cal)
        weather = forecast_weather(location)
        aqi_data = aqi(location)
        moon_phase_de = moon(weather['moon_phase'])
        
        #plain text email as backup
        text = email_text(weather, location, weekday, aqi_data, my_cal, wann_spielt_fc, last_match_fc, uselessfacts)
        print(text)

        #html email as primary
        html = email_html(weather, location, weekday, aqi_data, my_cal, wann_spielt_fc, last_match_fc, uselessfacts)

        #creating header of email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Das Wetter für " +str(location) +" am " +str(weekday)
        msg['From'] = email
        msg['To'] = receiver_email

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)
        #'''
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email, "xmtnrolasszlaihl")
        server.sendmail(email, receiver_email, msg.as_string())
        print("Email has been sent to " + receiver_email + "\n")
server.quit()
#'''
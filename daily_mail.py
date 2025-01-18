import smtplib

from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from helpers import forecast_weather, moon, email_text, email_html

email = "mgrundmo@gmail.com"
receiver_email = "mgrundmo@gmx.de"
location = "Hürth"

# list of adresses
adresses = [{'email': 'mgrundmo@gmx.de', 'location': 'Hürth'}, {'email': 'michael.grund@gmx.org', 'location': 'Bangkok'}]

for adresse in adresses:
    for i in adresse:
        print(adresse[i])

weather = forecast_weather(location)
moon_phase_de = moon(weather['moon_phase'])

#getting todays date and weekday
today = date.today()
weekday = today.strftime("%A, %d %B %Y")

#creating header of email
msg = MIMEMultipart('alternative')
msg['Subject'] = "Das Wetter für " +str(location) +" am " +str(weekday)
msg['From'] = email
msg['To'] = receiver_email

#plain text email as backup
text = email_text(weather, location, weekday)

#html email as primary
html = email_html(weather, location, weekday)

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)
print(text)
server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(email, "xmtnrolasszlaihl")

server.sendmail(email, receiver_email, msg.as_string())
server.quit()
print("Email has been sent to " + receiver_email)

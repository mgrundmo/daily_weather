import smtplib

from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from helpers import forecast_weather, moon

email = "mgrundmo@gmail.com"
receiver_email = "mgrundmo@gmx.de"
location = "Cologne"

weather = forecast_weather(location)
moon_phase_de = moon(weather['moon_phase'])

today = date.today()
weekday = today.strftime("%A, %d %B %Y")

msg = MIMEMultipart('alternative')
msg['Subject'] = "Das Wetter für " +str(location) +" am " +str(weekday)
msg['From'] = email
msg['To'] = receiver_email

#plain text email as backup
text = f"Das Wetter in {location} am {weekday}\n\n\
Hoechsttemperatur: {weather['temp_high']}C\n\
Tiefsttemperatur:  {weather['temp_low']}C\n\
Aussichten: {weather['condition']}\n\
Regen:  {weather['rain']} l/m2\n\
Schnee: {weather['snow']} cm\n\
------------------------\n\
Sonnenaufgang:   {weather['sunrise']}\n\
Sonnenuntergang: {weather['sunset']}\n\
------------------------\n\
Mondaufgang:     {weather['moonrise']}\n\
Monduntergang:   {weather['moonset']}\n\
Mondphase: {moon_phase_de}"

#html email as primary
html = '''\
<!DOCTYPE html>
<html>
<head>
<style>
body {
    font-family: Verdana, sans-serif;
}
table, td {
    border: 2px solid grey;
    border-radius: 5px;
    padding: 10px;
    margin: 5px;
}
td {
    width: 40%;
}
img {
    display: block;
    margin: auto;
}
</style>
</head>
    <body>
        <h2>Das Wetter in '''+str(location)+''' für '''+str(weekday)+'''</h2>
        <div style="width:100%;border:2px solid grey; border-radius: 5px; margin: 5px">
            <img src="https:'''+str(weather['icon'])+'''" alt="weather icon">
        </div>
        <table>
            <tr>
                <td>Höchsttemperatur:</td>
                <td>'''+str(weather['temp_high'])+''' °C</td>
            </tr>
            <tr>
                <td>Tiefsttemperatur:</td>
                <td>'''+str(weather['temp_low'])+''' °C</td>
            </tr>
            <tr>
                <td>Aussichten:</td>
                <td>'''+str(weather['condition'])+'''</td>
            </tr>
            <tr>
                <td>Regen:</td>
                <td>'''+str(weather['rain'])+''' l/m²</td>
            </tr>
            <tr>
                <td>Schnee:</td>
                <td>'''+str(weather['snow'])+''' cm</td>
            </tr>
        </table>
        <table>
            <tr>
                <td>Sonnenaufgang:</td>
                <td>'''+str(weather['sunrise'])+'''</td>
            </tr>
            <tr>
                <td>Sonnenuntergang:</td>
                <td>'''+str(weather['sunset'])+'''</td>
            </tr>
        </table>
        <table>
            <tr>
                <td>Mondaufgang:</td>
                <td>'''+str(weather['moonrise'])+'''</td>
            </tr>
            <tr>
                <td>Monduntergang:</td>
                <td>'''+str(weather['moonset'])+'''</td>
            </tr>
            <tr>
                <td>Mondphase:</td>
                <td>'''+str(moon_phase_de)+'''</td>
            </tr>
        </table>
    </body>
</html>
'''

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(email, "xmtnrolasszlaihl")

server.sendmail(email, receiver_email, msg.as_string())
server.quit()
print("Email has been sent to " + receiver_email)

import requests

from datetime import datetime
from quickstart import calendar

def forecast_weather(location):
    """Look up weather data for location."""
    key = "b97f0c7e03084663a3d81708242803"
    url = f"https://api.weatherapi.com/v1/forecast.json?key={key}&q={location}&days=1&aqi=yes&alert=no"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        weather_data = response.json()
        location_txt = weather_data["location"]["name"]        
        day_forecast = weather_data["forecast"]["forecastday"]
        date = day_forecast[0]["date"]
        temp_high = day_forecast[0]["day"]["maxtemp_c"]
        temp_low = day_forecast[0]["day"]["mintemp_c"]
        condition = day_forecast[0]["day"]["condition"]["text"]
        icon = day_forecast[0]["day"]["condition"]["icon"]
        rain = day_forecast[0]["day"]["totalprecip_mm"]
        snow = day_forecast[0]["day"]["totalsnow_cm"]
        wind = day_forecast[0]["day"]["maxwind_kph"]
        if snow > 0:
            snow_wind = str(snow) +" cm"
            snow_wind_lbl = "Schnee"
        else:
            snow_wind = str(wind) +" km/h"
            snow_wind_lbl = "Wind"
        sunrise = day_forecast[0]["astro"]["sunrise"]
        sunrise = timeconverter(sunrise)
        sunset = day_forecast[0]["astro"]["sunset"]
        sunset = timeconverter(sunset)
        moonrise = day_forecast[0]["astro"]["moonrise"]
        moonrise = timeconverter(moonrise)
        if("No" in moonrise):
            moonrise = 'Gestern'
        moonset = day_forecast[0]["astro"]["moonset"]
        moonset = timeconverter(moonset)
        if("No" in moonset):
            moonset = 'Morgen'
        moon_phase = day_forecast[0]["astro"]["moon_phase"]
        
        weather = {
            "date": date,
            "temp_high": temp_high,
            "temp_low": temp_low,
            "condition": condition,
            "icon":icon,
            "rain": rain,
            "snow_wind": snow_wind,
            "snow_wind_lbl": snow_wind_lbl,
            "sunrise": sunrise,
            "sunset": sunset,
            "moonrise": moonrise,
            "moonset": moonset,
            "moon_phase": moon_phase,
            "location": location_txt
        }                                  
        return weather
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None

def aqi(lat, lng):
    #preparing url for api request
    key = "e58b917a725410fd628f654b02205f90f2f781a4"
    location = f"geo:{lat};{lng}"
    url = f"https://api.waqi.info/feed/{location}/?token={key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        #receiving data from api server
        data = response.json()
        aqi_data = data["data"]["aqi"]
        if aqi_data > 50 and aqi_data < 151:
            aqi_text_color = "black"
            print(aqi_text_color)
        else:
            aqi_text_color = "white"

        if aqi_data < 51:
            aqi_status = "Gut"
            aqi_color = "#009966"
        elif aqi_data > 50 and aqi_data < 101:
            aqi_status = "Mäßig"
            aqi_color = "#ffde33"
        elif aqi_data > 100 and aqi_data < 151:
            aqi_status = "Ungesund für sensible Gruppen"
            aqi_color = "#ff9933"
        elif aqi_data > 150 and aqi_data < 201:
            aqi_status = "Ungesund"
            aqi_color = "#cc0033"
        elif aqi_data > 200 and aqi_data < 301:
            aqi_status = "Sehr ungesund"
            aqi_color = "#660099"
        else:
            aqi_status = "Gefährlich"
            aqi_color = "#7e0023"
        return(aqi_data, aqi_status, aqi_color, aqi_text_color)
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None

def last_fc():
    url_lg = f"https://api.openligadb.de/getlastmatchbyleagueteam/4755/65" #results for 2BL
    url_pk = f"https://api.openligadb.de/getlastmatchbyleagueteam/4739/65" #results for pokal
    url_next = f"https://api.openligadb.de/getnextmatchbyleagueteam/4755/65" #next match for 2BL
    try:
        response_lg = requests.get(url_lg)
        response_pk = requests.get(url_pk)
        response_next = requests.get(url_next)
        response_lg.raise_for_status()  # Raise an error for HTTP error responses
        response_pk.raise_for_status()  # Raise an error for HTTP error responses
        response_next.raise_for_status()  # Raise an error for HTTP error responses
        fc_data_lg = response_lg.json()
        fc_data_pk = response_pk.json()
        fc_data_next = response_next.json()
        date_time_lg = fc_data_lg['matchDateTime']
        date_lg = datetime.strptime(date_time_lg, '%Y-%m-%dT%H:%M:%S')
        date_time_pk = fc_data_pk['matchDateTime']
        date_pk = datetime.strptime(date_time_pk, '%Y-%m-%dT%H:%M:%S')
        if date_pk > date_lg:
            fc_data = fc_data_pk
        else:
            fc_data = fc_data_lg
        date_time_last = fc_data['matchDateTime']
        date_last = date_time_last[:10]
        team1_logo_last = fc_data['team1']['teamIconUrl']
        team1_name_last = fc_data['team1']['shortName']
        team2_logo_last = fc_data['team2']['teamIconUrl']
        team2_name_last = fc_data['team2']['shortName']
        result1 = fc_data['matchResults'][1]['pointsTeam1']
        result2 = fc_data['matchResults'][1]['pointsTeam2']
        last_match_fc = {
            "date": date_last,
            "team1_logo": team1_logo_last,
            "team1_name": team1_name_last,
            "team2_logo": team2_logo_last,
            "team2_name": team2_name_last,
            "result1": result1,
            "result2": result2
        }
        date_time_next = fc_data_next['matchDateTime']
        date_next = date_time_next[:10]
        team1_name_next = fc_data_next['team1']['teamName']
        team2_name_next = fc_data_next['team2']['teamName']
        next_match_fc = {
            "date": date_next,
            "team1_name": team1_name_next,
            "team2_name": team2_name_next,
        }
        next_fc = f"{next_match_fc['date']}                      {next_match_fc['team1_name']} : {next_match_fc['team2_name']}"
        return last_match_fc, next_fc
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None

def moon(phase_en):
    moon_phases = {
        "New Moon": "Neumond",
        "Waxing Crescent": "Zunehmende Sichel",
        "First Quarter": "Zunehmender Halbmond",
        "Waxing Gibbous": "Zunehmender Dreiviertelmond",
        "Full Moon": "Vollmond",
        "Waning Gibbous": "abnehmender Dreiviertelmond",
        "Last Quarter": "Abnehmender Halbmond",
        "Waning Crescent": "Abnehmende Sichel"
    }
    phase_de = moon_phases[phase_en]
    return phase_de

def useless_facts():
    url = f"https://uselessfacts.jsph.pl/api/v2/facts/random?language=de"
    response = requests.get(url)
    useless_facts = response.json()
    return useless_facts

def email_text(weather, weekday, aqi_data, wann_spielt_fc, last_match_fc, uselessfacts):
    moon_phase_de = moon(weather['moon_phase'])
    '''
    if my_cal:
        text_a = f"Die nächsten Termine: {my_cal[0]}\n\
                          {my_cal[1]}\n\
                          {my_cal[2]}\n\
                          {my_cal[3]}\n\
                          {my_cal[4]}"
    else:
        text_a = " "
    '''
    text = f"Das Wetter in {weather['location']} am {weekday}\n\n\
    Hoechsttemperatur: {weather['temp_high']}C\n\
    Tiefsttemperatur:  {weather['temp_low']}C\n\
    Aussichten: {weather['condition']}\n\
    Regen:  {weather['rain']} l/m2\n\
    {weather['snow_wind_lbl']}: {weather['snow_wind']}\n\
    Air Quality: {aqi_data[0]} / {aqi_data[1]}\n\
    ------------------------\n\
    Sonnenaufgang:   {weather['sunrise']}\n\
    Sonnenuntergang: {weather['sunset']}\n\
    ------------------------\n\
    Mondaufgang:     {weather['moonrise']}\n\
    Monduntergang:   {weather['moonset']}\n\
    Mondphase: {moon_phase_de}\n\
    Der FC spielt: {wann_spielt_fc}\n\
    Der FC hat gespielt:\
    {last_match_fc['date']}\
    {last_match_fc['team1_name']}\
    {last_match_fc['result1']}:{last_match_fc['result2']}\
    {last_match_fc['team2_name']}\n\
    Und sonst? {uselessfacts['text']}"
    return(text)

def email_html(weather, weekday, aqi_data, wann_spielt_fc, last_match_fc, uselessfacts):
    moon_phase_de = moon(weather['moon_phase'])
    html = '''\
    <!DOCTYPE html>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <html>
        <head>
            <style>
                body {
                    font-family: Verdana, sans-serif;
                }
                table, td {
                    border: 1px solid grey;
                    border-radius: 5px;
                    padding: 5px;
                    margin: 5px;
                }
                img {
                    display: block;
                    margin: auto;
                }
                .marquee {
                    overflow: hidden;
                    position: relative;
                    height: 25px;
                    width: 100%;
                    border: 1px solid grey;
                    border-radius: 5px;
                }
                .marquee p {
                    position: absolute;
                    margin: 0;
                    line-height: 25px;
                    white-space: nowrap;                   
                    animation: scroll-left 20s linear infinite;
                }
                @keyframes scroll-left {
                    0% {
                        transform: translateX(200%);
                    }
                    100% {
                        transform: translateX(-100%);
                    }
                }
            </style>
        </head>
        <body>
            <h2 style="text-align: center;">Das Wetter in '''+str(weather['location'])+''' für '''+str(weekday)+'''</h2>
            <div style="width:50%;border:1px solid grey; border-radius: 5px; margin: 5px">
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
                    <td>'''+str(weather['snow_wind_lbl'])+''':</td>
                    <td>'''+str(weather['snow_wind'])+'''</td>
                </tr>
                <tr>
                    <td>Luftqualität (AQI):</td>
                    <td style="color: '''+str(aqi_data[3])+'''; background-color: '''+str(aqi_data[2])+''';">'''+str(aqi_data[0])+'''</td>
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
            <h3>Wann spielt eigentlich der FC?</h3>
            <div class="marquee">
                <p>'''+str(wann_spielt_fc)+'''</p>
            </div>
            <h3>Und wie ist das letzte Spiel am '''+str(last_match_fc['date'])+''' ausgegangen?</h3>
            <table>
                <tr>
                    <td><img src="'''+str(last_match_fc['team1_logo'])+'''" alt="'''+str(last_match_fc['team1_name'])+'''" width="64"></td>
                    <td rowspan="2">'''+str(last_match_fc['result1'])+'''</td>
                    <td rowspan="2">'''+str(last_match_fc['result2'])+'''</td>
                    <td><img src="'''+str(last_match_fc['team2_logo'])+'''" alt="'''+str(last_match_fc['team2_name'])+'''" width="64"></td>
                </tr>
                <tr>
                    <td>'''+str(last_match_fc['team1_name'])+'''</td>
                    <td>'''+str(last_match_fc['team2_name'])+'''</td>
                </tr>
            </table>
            <h3>Und sonst?</h3>
            <p>'''+str(uselessfacts['text'])+'''</p>
        </body>
    </html>    
    '''
    return(html)

def timeconverter(time_12h):
    #converts AM/PM time format into 24h format'
    hour = time_12h[:2]
    minute = time_12h[2:-3]
    am_pm = time_12h[-2:]
    if am_pm == 'PM' and int(hour) < 12:
        num = int(hour) + 12
        hour = str(num)
    if am_pm == 'AM' and hour == '12':
        num = int(hour) - 12
        hour = str(num)
    time_24h = hour + minute
    return time_24h
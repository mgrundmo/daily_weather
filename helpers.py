import requests

from datetime import datetime

def forecast_weather(location):
    """Look up weather data for location."""
    key = "b97f0c7e03084663a3d81708242803"
    url = f"https://api.weatherapi.com/v1/forecast.json?key={key}&q={location}&days=1&aqi=yes&alert=no"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        weather_data = response.json()
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
            "moon_phase": moon_phase
        }                                  
        return weather
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None

def moon(phase_en):
    moon_phases = {
        "New": "Neumond",
        "Waxing Crescent": "Zunehmende Sichel",
        "First Quarter": "Zunehmender Halbmond",
        "Waxing Gibbous": "Zuhnemneder Dreiviertelmond",
        "Full": "Vollmond",
        "Waning Gibbous": "abnehmender Dreiviertelmond",
        "Last Quarter": "Abnehmender Halbmond",
        "Waning Crescent": "Abnehmende Sichel"
    }
    phase_de = moon_phases[phase_en]
    return phase_de

def email_text(weather, location, weekday):
    moon_phase_de = moon(weather['moon_phase'])

    text = f"Das Wetter in {location} am {weekday}\n\n\
    Hoechsttemperatur: {weather['temp_high']}C\n\
    Tiefsttemperatur:  {weather['temp_low']}C\n\
    Aussichten: {weather['condition']}\n\
    Regen:  {weather['rain']} l/m2\n\
    {weather['snow_wind_lbl']}: {weather['snow_wind']}\n\
    ------------------------\n\
    Sonnenaufgang:   {weather['sunrise']}\n\
    Sonnenuntergang: {weather['sunset']}\n\
    ------------------------\n\
    Mondaufgang:     {weather['moonrise']}\n\
    Monduntergang:   {weather['moonset']}\n\
    Mondphase: {moon_phase_de}"
    return(text)

def email_html(weather, location, weekday):
    moon_phase_de = moon(weather['moon_phase'])
    html = '''\
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                body {
                    font-family: Verdana, sans-serif;
                }
                table, th, td {
                    border: 2px solid grey;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 5px;
                    width: 50%;
                }
                img {
                    display: block;
                    margin: auto;
                }
            </style>
        </head>
        <body>
            <h2>Das Wetter in '''+str(location)+''' für '''+str(weekday)+'''</h2>
            <div style="width:50%;border:2px solid grey; border-radius: 5px; margin: 5px">
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
    return(html)

def timeconverter(time_12h):
    #converts AM/PM time format into 24h format'
    hour = time_12h[:2]
    minute = time_12h[2:-3]
    am_pm = time_12h[-2:]
    if am_pm == 'PM':
        num = int(hour) + 12
        hour = str(num)
    if am_pm == 'AM' and hour == '12':
        num = int(hour) - 12
        hour = str(num)
    time_24h = hour + minute
    return time_24h
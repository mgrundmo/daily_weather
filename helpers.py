import requests

from datetime import date

def forecast_weather(location):
    """Look up weather data for location."""
    key = "b97f0c7e03084663a3d81708242803"
    url = f"https://api.weatherapi.com/v1/forecast.json?key={key}&q={location}&days=1&aqi=no&alert=yes"
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
        sunrise = day_forecast[0]["astro"]["sunrise"]
        sunset = day_forecast[0]["astro"]["sunset"]
        moonrise = day_forecast[0]["astro"]["moonrise"]
        moonset = day_forecast[0]["astro"]["moonset"]
        moon_phase = day_forecast[0]["astro"]["moon_phase"]
        
        weather = {
            "date": date,
            "temp_high": temp_high,
            "temp_low": temp_low,
            "condition": condition,
            "icon":icon,
            "rain": rain,
            "snow": snow,
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
        "Third Quarter": "Abnehmender Halbmond",
        "Waning Crescent": "Abnehmende Sichel"
    }
    phase_de = moon_phases[phase_en]
    return phase_de
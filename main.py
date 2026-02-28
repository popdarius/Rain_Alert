import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


MY_LAT = 57.7089
MY_LONG = 11.9746

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "cnt": 8,  # next 24 hours
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()

will_rain = False

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=" Rain Alert! 🍃🌧☔💦"
             "Bring an umbrella in the next 24 hours",
        from_=os.getenv("TWILIO_NUMBER"),
        to=os.getenv("PHONE_NUMBER")
    )

    print(message.status)

import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv("./.env")

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

MY_LAT = 19.0760
MY_LON = 72.8777

API_KEY = os.getenv("API_KEY")
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

test_lat = 55.7558
test_lon = 37.6173

parameters = {
    "lat": test_lat,
    "lon": test_lon,
    "appid": API_KEY,
    "cnt": 4,
}


def send_mail():
    message = "Subject:Rain Alert!!\n\nCarry an umbrella."
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=message)


def check_weather():
    response = requests.get(url=API_ENDPOINT, params=parameters)
    response.raise_for_status()
    weather_data = response.json()
    weather_id_list = [weather_data['list'][i]['weather'][0]['id'] for i in range(4)]
    will_rain = False
    for i in weather_id_list:
        if i < 700:
            will_rain = True

    if will_rain:
        send_mail()
        print("mail sent")
    else:
        print("Dont worry, it won't rain")


check_weather()

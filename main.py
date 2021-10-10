import requests
from datetime import datetime
import smtplib
import time


MY_EMAIL = "pvcnya@gmail.com"
MY_PASSWORD = "pvcnya2013"

MY_LATITUDE = 32.181412
MY_LONGITUDE = 34.872669


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if iss_latitude - 5 <= MY_LATITUDE <= iss_latitude + 5 and iss_longitude - 5 <= MY_LONGITUDE <= iss_longitude + 5:
        return True


def is_it_night():
    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0,
    }

    response = requests.get(url=" https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    print(data)
    sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
    sunset = data["results"]["sunset"].split("T")[1].split(":")[0]
    # print(sunrise.split("T")[1].split(":")[0])
    print(sunset)
    time_now = datetime.now().hour

    if sunset < time_now < sunrise:
        return True


def send_email():
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="nirgalili1@gmail.com",
                            msg=f"Subject:LOOK UP\n\nThe ISS is over your head")

is_on = True
while is_on:
    if is_overhead() and is_it_night():
        send_email()
    time.sleep(60)

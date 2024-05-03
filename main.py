import requests
from datetime import datetime
import smtplib
import time

# ---------------------------- CONSTANTS ------------------------------- #\

my_email = ""
my_password = ""
my_lat = 30.733315
my_long = 76.779419

# ---------------------------- ABOVE OR NOT ------------------------------- #


def is_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if my_lat-5 <= iss_latitude <= my_lat+5 and my_long-5 <= iss_longitude <= my_long+5:
        return True

# ---------------------------- NIGHT OR NOT ------------------------------- #


def night_or_not():
    parameters = {
        "lat": my_lat,
        "lng": my_long,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if sunset < time_now < sunrise:
        return True

# ---------------------------- SENDING EMAIL ------------------------------- #


while True:
    time.sleep(60)
    if night_or_not() and is_above():
        try:
            connection = smtplib.SMTP("smtp.gmail.com", port=587)
            connection.starttls()
            connection.login(user=my_email, password=my_password)

        except smtplib.SMTPAuthenticationError:
            print("Authentication error")

        except smtplib.SMTPException as e:
            print("An error occured", e)

        else:
            from_addr = my_email
            to_addrs = {"", my_email}
            subject = "ISS IS ABOVE WATCH IT!"
            message = f"International Space station is above your head"
            email_body = f"Subject:{subject}\n\n{message}"
            connection.sendmail(from_addr, to_addrs, email_body)

        finally:
            connection.quit()

import requests
from datetime import datetime
import smtplib
import time
from twilio.rest import Client

# twilio API settings
account_sid = YOUR TWILIO ACCOUNT SID
auth_token = YOUR TWILIO AUTH TOKEN

# Creating twilio client
client = Client(account_sid, auth_token)

# e-mail and location settings
MY_EMAIL = YOUR EMAIL
MY_PASSWORD = YOUR PASSWORD
MY_LAT = YOUR LOCATION LAT  # You can find it on https://www.latlong.net/
MY_LONG = YOUR LOCATION LONG  # You can find it on https://www.latlong.net/

def main():
    while True:
        # Adding some time sleep in order to slow down the loop.
        time.sleep(60)
        if is_iss_overhead() and is_night():
            send_sms()
            send_email()

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the iss position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


def send_email():
    print("BINGO")
    connection = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=EMAIL WHERE THE MSG SHOULD BE SENT,
        msg="Subject:Look Up!\n\nThe ISS is above you in the sky."
    )

def send_sms():
    message = client.messages \
        .create(
        body="Look Up!\n\nThe ISS is above you in the sky.",
        from_=YOUR TWILIO NUMBER,
        to=NUMBER WHERE THE MSG SHOULD BE SENT
    )
    print(message.status)

if __name__ == "__main__":
    main()
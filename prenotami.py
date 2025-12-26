import requests
from requests_html import HTMLSession
import time
import smtplib
import os
from email.mime.text import MIMEText
import logging

# --- CONFIG ---
EMAIL = "ihebkhemiri1312x@gmail.com"
PASSWORD = "Hh123456@"  # Gmail app password, not real one you dumb fuck
ALERT_TO = "fallagiheb@gmail.com"
LOGIN_URL = "https://prenotami.esteri.it/Login"
BOOKING_URL = "https://prenotami.esteri.it/Services/Booking/2359"
SESSION_CHECK_INTERVAL = 10  # Check every 10 seconds — smooth like butter, not like a hammer
COOKIES_FILE = "cookies.pkl"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

logging.basicConfig(level=logging.INFO)

# --- EMAIL ALERT ---
def send_alert():
    msg = MIMEText(f"🔥 SLOT OPENED DICKHEAD: {BOOKING_URL}")
    msg["Subject"] = "SLOT FUCKING OPEN - GO GO GO"
    msg["From"] = EMAIL
    msg["To"] = ALERT_TO

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, ALERT_TO, msg.as_string())
        print("✅ ALERT SENT YOU LAZY SHIT")
    except Exception as e:
        print(f"🚨 EMAIL FAILED: {e}")

# --- MAIN MONITOR ---
def monitor_slot():
    session = HTMLSession()
    session.headers.update({"User-Agent": USER_AGENT})

    # Login first
    print("🔐 Logging in... you better have valid creds, idiot")
    login_res = session.get(LOGIN_URL)
    csrf = login_res.html.find('input[name="__RequestVerificationToken"]', first=True).attrs['value']

    login_payload = {
        "Username": "iheb.khemiri@yassir.com",
        "Password": "Iheb2025@",
        "__RequestVerificationToken": csrf
    }

    res = session.post(LOGIN_URL, data=login_payload)
    if "Login" in res.url or "error" in res.text.lower():
        print("💀 LOGIN FAILED — CHECK YOUR FUCKING CREDENTIALS")
        return

    print("✅ Logged in, baby. Now hunting...")

    while True:
        try:
            # GET the booking URL — if we stay on it, it's OPEN
            res = session.get(BOOKING_URL, allow_redirects=False)
            
            if res.status_code == 200 and BOOKING_URL in res.url:
                print("🎉🎉🎉 HOLY SHIT — SLOT IS OPEN! GO GO GO!")
                send_alert()
                time.sleep(300)  # Alert once, then chill for 5 mins
            else:
                print(f"🔒 Still closed (Status: {res.status_code}) — trying again in {SESSION_CHECK_INTERVAL}s")

        except Exception as e:
            print(f"💥 Crash: {e} — but we don't give a fuck, retrying...")
        
        time.sleep(SESSION_CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_slot()

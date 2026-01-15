"""
mail_automation_secure.py
Send email automatically using environment variables for credentials.
"""

import smtplib
import os
from email.message import EmailMessage

def send_email():
    # Load credentials from environment variables
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        print("Email credentials are not set")
        return

    msg = EmailMessage()
    msg["Subject"] = "Automation Test Email"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("This email was sent automatically using Python.")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)

if __name__ == "__main__":
    send_email()

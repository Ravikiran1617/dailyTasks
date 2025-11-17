import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_registeration_email_to_user(email: str):
    """Send a welcome email after successful registration"""

    subject = "Welcome to Our Platform!"
    body = f"""
    Hi,

    Your registration is successful. 
    Thank you for joining our platform.

    Regards,
    Team Support
    """

    send_email(email, subject, body)


def send_login_success_email(email: str):
    """Send login success email"""
    
    subject = "Login Successful"
    body = f"""
    Hello,

    You have successfully logged into your account.

    If this wasn't you, please secure your account immediately.

    Regards,
    Team Support
    """

    send_email(email, subject, body)


def send_email(to_email: str, subject: str, body: str):
    """Generic function to send an email via SMTP"""

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
    except Exception as e:
        print("Email Error:", e)

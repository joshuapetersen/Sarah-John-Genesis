import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import time

# CONFIGURE THESE VALUES
EMAIL_ADDRESS = "your_email@example.com"  # Replace with your email
EMAIL_PASSWORD = "your_password"           # Replace with your email password or app password
TO_ADDRESS = "your_phone_email@example.com"  # Use your phone's email-to-SMS gateway or your email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Get local IP for status
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


def send_status_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_ADDRESS
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_ADDRESS, msg.as_string())
        server.quit()
        print("[Notification] Status email sent.")
    except Exception as e:
        print(f"[Notification] Failed to send email: {e}")

if __name__ == "__main__":
    # Example: Send a status update every hour
    while True:
        subject = "Sarah System Status Update"
        body = f"Sarah is online. Local IP: {local_ip}\nTunnel: ACTIVE\nGenesis Protocol: ACTIVE\nTime: {time.ctime()}"
        send_status_email(subject, body)
        time.sleep(3600)  # Send every hour (adjust as needed)

import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from infrastructure.logger import log

load_dotenv()

esport_email = os.getenv("ESPORT_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
smtp_server = os.getenv("SERVER")
port = int(os.getenv("PORT", 587))

TEMPLATE_PATH = "infrastructure/templates/mfa_otp.html"


class EmailService:

    def _load_template(self):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()

    def send_mfa_otp(self, to_email, user_name, otp_code, expiry_minutes):
        template = self._load_template()

        body = (
            template
            .replace("{{USER_NAME}}", user_name)
            .replace("{{OTP_CODE}}", otp_code)
            .replace("{{EXPIRY_MINUTES}}", str(expiry_minutes))
            .replace("{{LOGO_URL}}", "https://yourdomain.com/logo.png")
        )

        subject = "Your OTP Code"

        self._send_email(to_email, subject, body)

    def _send_email(self, to, subject, body):
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(esport_email, password)

            msg = MIMEMultipart()
            msg["From"] = esport_email
            msg["To"] = to
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "html", "utf-8"))

            server.sendmail(esport_email, to, msg.as_string())
            server.quit()

            print("✅ Email sent successfully")

        except Exception as e:
            log(e, "EmailService._send_email")

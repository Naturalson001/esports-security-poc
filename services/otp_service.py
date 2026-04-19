import time
import hashlib
import os

from infrastructure.logger import log
from services.email_service import EmailService

secret_key = os.getenv("SECRET_KEY")

class OtpService:
    otp_store = {}

    def __init__(self):
        self.email_service = EmailService()

    def generate_otp(self, username):
        # 5-minute time window
        time_block = int(time.time() // 300)

        raw_value = f"{username}{secret_key}{time_block}"

        hashed = hashlib.sha256(raw_value.encode()).hexdigest()

        otp = str(int(hashed[:10], 16) % 100000).zfill(5)

        return otp

    def send_login_otp(self, email, user_name):
        otp = self.generate_otp(user_name)

        OtpService.otp_store[email] = {
            "otp": otp,
            "expires_at": time.time() + 300  # 5 minutes
        }

        log(f"OTP generated for {email}", "OtpService.send_login_otp", "INFO")

        self.email_service.send_mfa_otp(
            to_email=email,
            user_name=user_name,
            otp_code=otp,
            expiry_minutes=5
        )

        return otp

    def verify_otp(self, email, otp_code):
        record = OtpService.otp_store.get(email)

        if not record:
            return False

        if time.time() > record["expires_at"]:
            del self.otp_store[email]
            return False

        if record["otp"] == otp_code:
            del self.otp_store[email]
            return True

        return False
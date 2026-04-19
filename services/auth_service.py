from Helpers.hashing import HashedData
from services.otp_service import OtpService
from validators.user_validator import UserValidator
from infrastructure.database import (
    save_user,
    fetch_all_users,
    get_user_by_email
)


class AuthService:
    def __init__(self, otp_service):
        self.otp_service = otp_service

    def register_user(self,user):
        errors = UserValidator.validate_user(user)

        if errors:
            return {
                "success": False,
                "errors": errors,
                "status": 400
            }

        if UserValidator.email_exists(user.email):
            return {
                "success": False,
                "errors": ["Email already exists"],
                "status": 400
            }

        if UserValidator.username_exists(user.username):
            return {
                "success": False,
                "errors": ["Username already exists"],
                "status": 400
            }

        hashed_password = HashedData.generate_hash(user.password)

        user.password = hashed_password

        save_user(user)

        return {
            "success": True,
            "message": "User registered successfully"
        }

    def login_user(self, login_model):

        errors = UserValidator.validate_login(login_model)

        if errors:
            return {
                "success": False,
                "errors": errors,
                "status": 400
            }
        user = get_user_by_email(login_model.email)

        if not user:
            return {
                "success": False,
                "errors": ["User not found"],
                "status": 404
            }

        otp = self.otp_service.send_login_otp(
            login_model.email,
            user["username"],
        )

        if not otp:
            return {
                "success": False,
                "errors": ["Failed to generate OTP"],
                "status": 500
            }

        return {
            "success": True,
            "message": f"OTP sent successfully to {login_model.email}",
            "status": 200
        }

    def verify_login(self, otp_model):

            otp_verified = self.otp_service.verify_otp(
                otp_model.email,
                otp_model.otp )

            if not otp_verified:
                return {
                    "success": False,
                    "errors" : ["OTP verification failed"],
                    "status": 401
                }

            return {
                "success": True,
                "message": "Login successful",
                "status": 200
            }

    def get_all_users(self, current_user):
        if not current_user:
            return {
                "success": False,
                "errors": ["User not found"],
                "status": 404
            }

        if current_user["role"].lower() != "admin":
            return {
                "success": False,
                "errors": ["Access denied"],
                "status": 403
            }

        users = fetch_all_users()

        return {
            "success": True,
            "data": users,
            "status": 200
        }




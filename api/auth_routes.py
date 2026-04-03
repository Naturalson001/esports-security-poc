from fastapi import APIRouter
from services.auth_service import AuthService
from models.user_model import UserModel
from models.login_model import LoginModel
from models.otp_model import OtpModel
from services.otp_service import OtpService

router = APIRouter(prefix="/v1/auth")

otp_service = OtpService()
auth_service = AuthService(otp_service)

@router.post("/register")
def register(user: UserModel):
    return auth_service.register_user(user)

@router.post("/login")
def login(data: LoginModel):
    return auth_service.login_user(data)

@router.post("/verify-otp")
def verify(data: OtpModel):
    return auth_service.verify_login(data)

@router.get("/get-users")
def get_users():
    return auth_service.get_all_users()
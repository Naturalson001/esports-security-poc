from pydantic import BaseModel

class OtpModel(BaseModel):
    email: str
    otp: str
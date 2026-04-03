from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    twitch: str | None = None
    discord: str | None = None
    steam: str | None = None
    role: str = "gamer"
    coin: str | None = None
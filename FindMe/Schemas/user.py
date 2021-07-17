from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from hashlib import md5


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @validator('password', pre=True)
    def pw_creation(cls, v: str):
        if len(v) < 5:
            raise ValueError("Password too short")
        hashed_pw = md5(v.encode()).hexdigest()
        return hashed_pw

    @validator('email', pre=True)
    def email_lower(cls, v: str):
        return v.lower()


class UserRegister(UserLogin):
    name: str


class TokenJWT(BaseModel):
    access_token: str
    refresh_token: Optional[str]
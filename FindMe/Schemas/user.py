from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from FindMe.Schemas import tasks
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
    username: str

    @validator('username', pre=True)
    def username_check(cls, v: str):
        if v.isalnum():
            return v.lower()
        raise ValueError('not valid username, should be alphanum')


class UserInfo(BaseModel):
    name: str
    username: str
    display_picture: str
    score: int

    @validator('display_picture', pre=True)
    def display_picture_check(cls, v: Optional[str]):
        if v is None:
            return 'https://storage.googleapis.com/bvhacks/default.jpg'
        return v

    class Config:
        orm_mode = True


class CompleteUserInfo(UserInfo):
    tasks_added: List[tasks.TaskOverview]
    task_completed: List[tasks.TaskOverview]

    class Config:
        orm_mode = True


class TokenJWT(BaseModel):
    access_token: str
    refresh_token: Optional[str]

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    email: str
    full_name: str
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class NewUser(User):
    password: str

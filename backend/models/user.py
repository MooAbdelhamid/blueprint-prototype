""" """

from pydantic import BaseModel


class UserRegister(BaseModel):
    user: str
    email: str
    password: str

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from typing import Literal


class UserSignup(BaseModel):

    email: EmailStr

    username: str

    password: str = Field(
        ...,
        min_length=6
    )

    role: Literal[
        "student",
        "teacher",
        "school"
    ]


class UserLogin(BaseModel):

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6
    )
class UpdateProfile(BaseModel):

    name: str

    bio: str

    phone: str
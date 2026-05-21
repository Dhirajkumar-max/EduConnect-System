from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6
    )
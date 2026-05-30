from pydantic import BaseModel


class MessageModel(BaseModel):

    receiver_email: str

    message: str
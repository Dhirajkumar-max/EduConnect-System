from pydantic import BaseModel

class School(BaseModel):
    name: str
    address: str
    principal: str
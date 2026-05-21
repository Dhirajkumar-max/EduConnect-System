from pydantic import BaseModel, Field

class School(BaseModel):

    name: str = Field(..., min_length=3, max_length=100)

    address: str = Field(..., min_length=3, max_length=200)

    principal: str = Field(..., min_length=3, max_length=100)
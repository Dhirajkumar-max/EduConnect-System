from pydantic import BaseModel
from typing import Optional, Literal


class PostCreate(BaseModel):
     
    title:str

    content: str

    image_url: Optional[str] = None

    video_url: Optional[str] = None
    audience: Literal["community", "students", "teachers", "schools"] = "community"

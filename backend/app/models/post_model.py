from pydantic import BaseModel
from typing import Optional


class PostCreate(BaseModel):
     
    title:str

    content: str

    image_url: Optional[str] = None

    video_url: Optional[str] = None
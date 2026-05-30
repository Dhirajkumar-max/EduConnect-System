from pydantic import BaseModel


class CourseModel(BaseModel):

    title: str

    description: str

    category: str
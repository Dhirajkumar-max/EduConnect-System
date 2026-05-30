from pydantic import BaseModel


class TeacherApplicationModel(BaseModel):

    school_email: str

    full_name: str

    subject: str

    experience: str

    qualifications: str

    area_of_interest: str

    skills: str

    certificates_url: str

    cv_url: str
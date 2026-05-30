from pydantic import BaseModel
class AdmissionModel(BaseModel):
    school_email: str
    full_name: str
    age: int
    class_name:str
    parent_email:str
    parent_contact: int
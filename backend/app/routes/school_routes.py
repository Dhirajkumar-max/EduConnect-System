from fastapi import APIRouter
from app.models.school_model import School
from app.database.connection import database

router = APIRouter()

@router.post("/add-school")
async def add_school(school: School):

    school_data = school.dict()

    result = await database.schools.insert_one(school_data)

    return {
        "message": "School added successfully",
        "id": str(result.inserted_id)
    }
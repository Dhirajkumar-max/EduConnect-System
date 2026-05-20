from fastapi import APIRouter
from bson import ObjectId
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

@router.get("/schools")
async def get_schools():

    schools = []

    async for school in database.schools.find():

        school["_id"] = str(school["_id"])

        schools.append(school)

    return {
        "schools": schools
    }

@router.get("/school/{school_id}")
async def get_school(school_id: str):

    school = await database.schools.find_one(
        {"_id": ObjectId(school_id)}
    )

    if school:

        school["_id"] = str(school["_id"])

        return school

    return {
        "message": "School not found"
    }
@router.put("/update-school/{school_id}")
async def update_school(school_id: str, school: School):

    updated_data = school.dict()

    result = await database.schools.update_one(
        {"_id": ObjectId(school_id)},
        {"$set": updated_data}
    )

    if result.modified_count == 1:
        return {
            "message": "School updated successfully"
        }

    return {
        "message": "School not found or no changes made"
    }
@router.delete("/delete-school/{school_id}")
async def delete_school(school_id: str):

    result = await database.schools.delete_one(
        {"_id": ObjectId(school_id)}
    )

    if result.deleted_count == 1:

        return {
            "message": "School deleted successfully"
        }

    return {
        "message": "School not found"
    }
from fastapi import APIRouter
from bson import ObjectId
from app.models.school_model import School
from app.database.connection import database
from bson import ObjectId
from fastapi import HTTPException
from app.services.school_service import (
    create_school,
    get_all_schools,
    get_school_by_id,
    update_school_by_id,
    delete_school_by_id
)

router = APIRouter()

@router.post("/add-school")
async def add_school(school: School):

    school_data = school.dict()

    school_id = await create_school(school_data)

    return {
        "message": "School added successfully",
        "id": school_id
    }

@router.get("/schools")
async def get_schools():

    schools = await get_all_schools()

    return schools

@router.get("/school/{school_id}")
async def get_school(school_id: str):

    try:

        school = await get_school_by_id(school_id)

        if school:

            return school

        raise HTTPException(
            status_code=404,
            detail="School not found"
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid school ID"
        )
@router.put("/update-school/{school_id}")
async def update_school(school_id: str, school: School):

    try:

        updated_data = school.dict()

        updated = await update_school_by_id(
            school_id,
            updated_data
        )

        if updated == 1:

            return {
                "message": "School updated successfully"
            }

        raise HTTPException(
            status_code=404,
            detail="School not found"
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid school ID"
        )
@router.delete("/delete-school/{school_id}")
async def delete_school(school_id: str):

    try:

        deleted = await delete_school_by_id(school_id)

        if deleted == 1:

            return {
                "message": "School deleted successfully"
            }

        raise HTTPException(
            status_code=404,
            detail="School not found"
        )

    except:

        raise HTTPException(
            status_code=400,
            detail="Invalid school ID"
        )
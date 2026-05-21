from app.database.connection import database
from bson import ObjectId


async def create_school(school_data):

    result = await database.schools.insert_one(school_data)

    return str(result.inserted_id)


async def get_all_schools():

    schools = []

    async for school in database.schools.find():

        school["_id"] = str(school["_id"])

        schools.append(school)

    return schools

async def get_school_by_id(school_id):

    school = await database.schools.find_one(
        {"_id": ObjectId(school_id)}
    )

    if school:

        school["_id"] = str(school["_id"])

    return school


async def update_school_by_id(school_id, updated_data):

    result = await database.schools.update_one(
        {"_id": ObjectId(school_id)},
        {"$set": updated_data}
    )

    return result.modified_count


async def delete_school_by_id(school_id):

    result = await database.schools.delete_one(
        {"_id": ObjectId(school_id)}
    )

    return result.deleted_count
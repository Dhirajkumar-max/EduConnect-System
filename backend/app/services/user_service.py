from app.database.connection import database


async def create_user(user_data):

    result = await database.users.insert_one(
        user_data
    )

    return str(result.inserted_id)


async def get_user_by_email(email):

    user = await database.users.find_one(
        {"email": email}
    )

    return user
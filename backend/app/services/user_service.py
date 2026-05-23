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

async def update_user_profile(
    email: str,
    profile_data: dict
):

    result = await database.users.update_one(
        {"email": email},
        {
            "$set": profile_data
        }
    )

    return result
async def get_all_users():

    users = await database.users.find().to_list(100)

    return users

async def get_users_by_role(role: str):

    users = await database.users.find(
        {"role": role}
    ).to_list(100)

    return users
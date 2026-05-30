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

async def follow_user(
    current_user_email,
    target_email
):

    # Current user following update
    await database.users.update_one(
        {
            "email": current_user_email
        },
        {
            "$addToSet": {
                "following": target_email
            }
        }
    )

    # Target user followers update
    await database.users.update_one(
        {
            "email": target_email
        },
        {
            "$addToSet": {
                "followers": current_user_email
            }
        }
    )

from bson import ObjectId


async def save_post(
    user_email,
    post_id
):

    result = await database.users.update_one(
        {
            "email": user_email
        },
        {
            "$addToSet": {
                "saved_posts": post_id
            }
        }
    )

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)

    return result


async def search_users(keyword):

    users = await database.users.find(
        {
            "username": {
                "$regex": keyword,
                "$options": "i"
            }
        }
    ).to_list(100)

    return users

async def get_user_by_username(
    username
):

    user = await database.users.find_one(
        {
            "username": username
        }
    )

    return user

async def add_notification(
    email,
    message
):

    result = await database.users.update_one(
        {
            "email": email
        },
        {
            "$push": {
                "notifications": message
            }
        }
    )

    return result

async def send_message(
    sender,
    receiver,
    message
):

    message_data = {
        "sender": sender,
        "receiver": receiver,
        "message": message
    }

    result = await database.messages.insert_one(
        message_data
    )

    return str(result.inserted_id)

async def get_my_messages(
    email
):

    messages = await database.messages.find(
        {
            "receiver": email
        }
    ).to_list(100)

    return messages

async def get_chat_between_users(
    user1,
    user2
):

    messages = await database.messages.find(
        {
            "$or": [
                {
                    "sender": user1,
                    "receiver": user2
                },
                {
                    "sender": user2,
                    "receiver": user1
                }
            ]
        }
    ).to_list(100)

    return messages
async def set_user_online(
    email
):

    result = await database.users.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "is_online": True
            }
        }
    )

    return result

async def get_online_users():

    users = await database.users.find(
        {
            "is_online": True
        }
    ).to_list(100)

    return users

async def upload_note(
    note_data
):

    result = await database.notes.insert_one(
        note_data
    )

    return str(result.inserted_id)

async def get_all_notes():

    notes = await database.notes.find().to_list(100)

    return notes

async def create_course(
    course_data
):

    result = await database.courses.insert_one(
        course_data
    )

    return str(result.inserted_id)

async def get_all_courses():

    courses = await database.courses.find().to_list(100)

    return courses

async def enroll_course(
    email,
    course_id
):

    result = await database.users.update_one(
        {
            "email": email
        },
        {
            "$addToSet": {
                "enrolled_courses": course_id
            }
        }
    )

    return result

async def get_my_enrollments(
    email
):

    user = await database.users.find_one(
        {
            "email": email
        }
    )

    return user.get(
        "enrolled_courses",
        []
    )

async def apply_admission(
        admission_data
):
    result = await database.admissions.insert_one(
        admission_data
    )

    return str(result.inserted_id)

async def get_school_applications(
    school_email
):

    applications = await database.admissions.find(
        {
            "school_email": school_email
        }
    ).to_list(100)

    return applications

async def apply_to_school(
    application_data
):

    result = await database.teacher_applications.insert_one(
        application_data
    )

    return str(result.inserted_id)

async def get_teacher_applications(
    school_email
):

    applications = await database.teacher_applications.find(
        {
            "school_email": school_email
        }
    ).to_list(100)

    return applications

async def verify_user(
    email
):

    result = await database.users.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "is_verified": True
            }
        }
    )

    return result

async def ban_user(
    email
):

    result = await database.users.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "is_banned": True
            }
        }
    )

    return result

from bson import ObjectId

async def update_admission_status(
    admission_id,
    status
):
    result = await database.admissions.update_one(
        {
            "_id": ObjectId(admission_id)
        },
        {
            "$set": {
                "status": status
            }
        }
    )

    return result.modified_count

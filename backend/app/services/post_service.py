from app.database.connection import database
from bson import ObjectId


async def create_post(post_data):

    result = await database.posts.insert_one(
        post_data
    )

    return str(result.inserted_id)


async def get_all_posts():

    posts = await database.posts.find().to_list(100)

    return posts

async def like_post(post_id):

    result = await database.posts.update_one(
        {
            "_id": ObjectId(post_id)
        },
        {
            "$inc": {
                "likes": 1
            }
        }
    )

    return result

async def comment_on_post(
    post_id,
    comment_data
):

    result = await database.posts.update_one(
        {
            "_id": ObjectId(post_id)
        },
        {
            "$push": {
                "comments": comment_data
            }
        }
    )

    return result

async def delete_post(post_id):

    result = await database.posts.delete_one(
        {
            "_id": ObjectId(post_id)
        }
    )

    return result
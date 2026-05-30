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

async def get_feed_posts(following_list):

    posts = await database.posts.find(
        {
            "created_by": {
                "$in": following_list
            }
        }
    ).to_list(100)

    return posts

async def get_posts_by_username(
    username
):

    posts = await database.posts.find(
        {
            "username": username
        }
    ).to_list(100)

    return posts

async def get_post_comments(
    post_id
):

    post = await database.posts.find_one(
        {
            "_id": ObjectId(post_id)
        }
    )

    return post.get("comments", [])
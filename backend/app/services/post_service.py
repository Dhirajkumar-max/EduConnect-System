from app.database.connection import database
from bson import ObjectId


async def create_post(post_data):

    result = await database.posts.insert_one(
        post_data
    )

    return str(result.inserted_id)


async def get_all_posts(role=None):

    query = {"$or": [{"visible_to": role}, {"visible_to": {"$exists": False}}]} if role else {}
    posts = await database.posts.find(query).sort("created_at", -1).to_list(100)

    return posts

async def toggle_like(post_id, email):
    post = await database.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        return None
    if email in post.get("liked_by", []):
        await database.posts.update_one({"_id": post["_id"]}, {"$pull": {"liked_by": email}, "$inc": {"likes": -1}})
        return False

    await database.posts.update_one(
        {
            "_id": ObjectId(post_id)
        },
        {
            "$addToSet": {"liked_by": email},
            "$inc": {"likes": 1}
        }
    )

    return True

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

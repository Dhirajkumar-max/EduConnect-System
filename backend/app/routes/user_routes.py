from fastapi import APIRouter, HTTPException

from app.utils.auth import (
    teacher_only,
    student_only,
    school_only,
    admin_only,
    get_current_user
)

from app.models.user_model import (
    UserSignup,
    UserLogin,
    UpdateProfile
)

from app.services.user_service import (
    create_user,
    get_user_by_email,
    update_user_profile,
    get_all_users,
    get_users_by_role
)
from fastapi import Depends

from app.utils.auth_bearer import JWTBearer

from app.utils.hash import hash_password

from app.models.post_model import CreatePost

from app.services.post_service import (
    create_post,
    get_all_posts,
    like_post,
    comment_on_post,
    delete_post
)

router = APIRouter()


@router.post("/signup")
async def signup(user: UserSignup):

    existing_user = await get_user_by_email(
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    user_data = {
        "email": user.email,
        "password": hashed_password,
        "role": user.role
    }

    user_id = await create_user(user_data)

    return {
        "message": "User created successfully",
        "id": user_id
    }

@router.post("/login")
async def login(user: UserLogin):

    existing_user = await get_user_by_email(
        user.email
    )

    if not existing_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    valid_password = verify_password(
        user.password,
        existing_user["password"]
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={
            "email": user.email,
            "role": existing_user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
from app.utils.hash import verify_password

from app.utils.jwt_handler import (
    create_access_token
)
@router.get(
    "/profile",
    dependencies=[Depends(JWTBearer())]
)
async def profile():

    return {
        "message": "Welcome to protected profile route"
    }
@router.get("/teacher-dashboard")
async def teacher_dashboard(
    user = Depends(teacher_only)
):

    return {
        "message": "Welcome Teacher Dashboard",
        "user": user
    }
@router.get("/student-dashboard")
async def student_dashboard (
    user = Depends(student_only)
):
    return{
        "message":"welcome student",
        "user":user
    }
@router.get("/school-dashboard")
async def school_dashboard(
    user = Depends(school_only)
):

    return {
        "message": "Welcome School Dashboard",
        "user": user
    }


@router.get("/admin-dashboard")
async def admin_dashboard(
    user = Depends(admin_only)
):

    return {
        "message": "Welcome Admin Dashboard",
        "user": user
    }

@router.get("/me")
async def get_my_profile(
    user = Depends(get_current_user)
):

    return {
        "message": "My Profile",
        "user": user
    }
@router.put("/update-profile")
async def update_profile(
    profile: UpdateProfile,
    user = Depends(get_current_user)
):

    profile_data = {
        "name": profile.name,
        "bio": profile.bio,
        "phone": profile.phone
    }

    await update_user_profile(
        user["email"],
        profile_data
    )

    return {
        "message": "Profile Updated Successfully",
        "data": profile_data
    }
@router.get("/my-profile")
async def my_profile(
    user = Depends(get_current_user)
):

    existing_user = await get_user_by_email(
        user["email"]
    )

    return {
        "message": "My Profile",
        "profile": {
            "email": existing_user["email"],
            "role": existing_user["role"],
            "name": existing_user.get("name"),
            "bio": existing_user.get("bio"),
            "phone": existing_user.get("phone")
        }
    }

@router.get("/all-users")
async def all_users():

    users = await get_all_users()

    clean_users = []

    for user in users:

        clean_users.append({
            "email": user.get("email"),
            "role": user.get("role"),
            "name": user.get("name"),
            "bio": user.get("bio")
        })

    return {
        "total_users": len(clean_users),
        "users": clean_users
    }

@router.get("/teachers")
async def get_teachers():

    teachers = await get_users_by_role(
        "teacher"
    )

    clean_teachers = []

    for teacher in teachers:

        clean_teachers.append({
            "email": teacher.get("email"),
            "name": teacher.get("name"),
            "bio": teacher.get("bio")
        })

    return {
        "total_teachers": len(clean_teachers),
        "teachers": clean_teachers
    }

@router.get("/schools")
async def get_schools():

    schools = await get_users_by_role(
        "school"
    )

    clean_schools = []

    for school in schools:

        clean_schools.append({
            "email": school.get("email"),
            "name": school.get("name"),
            "bio": school.get("bio")
        })

    return {
        "total_schools": len(clean_schools),
        "schools": clean_schools
    }

@router.get("/students")
async def get_students():

    students = await get_users_by_role(
        "student"
    )

    clean_students = []

    for student in students:

        clean_students.append({
            "email": student.get("email"),
            "name": student.get("name"),
            "bio": student.get("bio")
        })

    return {
        "total_students": len(clean_students),
        "students": clean_students
    }

@router.post("/create-post")
async def create_new_post(
    post: CreatePost,
    user = Depends(get_current_user)
):

    post_data = {
        "title": post.title,
        "content": post.content,
        "created_by": user["email"],
        "role": user["role"]
    }

    post_id = await create_post(
        post_data
    )

    return {
        "message": "Post Created Successfully",
        "post_id": post_id
    }

@router.get("/all-posts")
async def all_posts():

    posts = await get_all_posts()

    clean_posts = []

    for post in posts:

        clean_posts.append({
            "title": post.get("title"),
            "content": post.get("content"),
            "created_by": post.get("created_by"),
            "role": post.get("role"),
            "likes": post.get("likes", 0),
            "comments": post.get("comments", [])
            })

    return {
        "total_posts": len(clean_posts),
        "posts": clean_posts
    }

@router.post("/like-post/{post_id}")
async def like_a_post(post_id: str):

    await like_post(post_id)

    return {
        "message": "Post Liked Successfully"
    }

@router.post("/comment-post/{post_id}")
async def comment_post(
    post_id: str,
    comment: str,
    user = Depends(get_current_user)
):

    comment_data = {
        "comment": comment,
        "commented_by": user["email"]
    }

    await comment_on_post(
        post_id,
        comment_data
    )

    return {
        "message": "Comment Added Successfully"
    }

@router.delete("/delete-post/{post_id}")
async def remove_post(post_id: str):

    await delete_post(post_id)

    return {
        "message": "Post Deleted Successfully"
    }


from fastapi import APIRouter, HTTPException
from app.models.course_model import CourseModel
from fastapi import UploadFile, File
import cloudinary.uploader
from app.utils.cloudinary_config import *
from app.models.admission_model import (
    AdmissionModel
)

from app.models.teacher_application_model import (
    TeacherApplicationModel
)

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
    get_users_by_role,
    follow_user,
    save_post as save_post_service,
    search_users,
    get_user_by_username,
    add_notification,
    send_message,
    get_my_messages,
    get_chat_between_users,
    set_user_online,
    get_online_users,
    upload_note,
    get_all_notes,
    create_course,
    get_all_courses,
    enroll_course,
    get_my_enrollments,
    apply_admission,
    get_school_applications,
    apply_to_school,
    get_teacher_applications,
    verify_user,
    ban_user,
    get_school_applications,
    update_admission_status
)

from app.models.note_model import (
    NoteModel
)

from app.models.message_model import (
    MessageModel
)


from fastapi import Depends

from app.utils.auth_bearer import JWTBearer

from app.utils.hash import hash_password

from app.models.post_model import PostCreate

from app.services.post_service import (
    create_post,
    get_all_posts,
    like_post,
    comment_on_post,
    delete_post,
    get_feed_posts,
    get_posts_by_username,
    get_post_comments
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
        "username": user.username,
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
    
    if existing_user.get("is_banned"):

     raise HTTPException(
        status_code=403,
        detail="Your account has been banned"
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
    post: PostCreate,
    user = Depends(get_current_user)
):

    post_data = {
        "title": post.title,
        "content": post.content,
        "image_url": post.image_url,
        "video_url": post.video_url,
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
            "image_url": post.get("image_url"),
            "video_url": post.get("video_url"),
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

@router.post("/follow/{email}")
async def follow(
    email: str,
    user = Depends(get_current_user)
):

    await follow_user(
        user["email"],
        email
    )
    await add_notification(
    email,
    f"{user['email']} started following you"
    )

    return {
        "message": f"You are now following {email}"
    }


@router.get("/my-following")
async def my_following(
    user = Depends(get_current_user)
):

    return {
        "email": user["email"],
        "following": user.get("following", [])
    }

@router.get("/feed")
async def get_feed(
    user = Depends(get_current_user)
):

    following = user.get(
        "following",
        []
    )

    posts = await get_feed_posts(
        following
    )

    clean_posts = []

    for post in posts:

        clean_posts.append({
            "id": str(post["_id"]),
            "title": post.get("title"),
            "content": post.get("content"),
            "created_by": post.get("created_by"),
            "role": post.get("role"),
            "likes": post.get("likes", 0),
            "comments": post.get("comments", [])
        })

    return {
        "feed_posts": clean_posts
    }

@router.get("/my-followers")
async def my_followers(
    user = Depends(get_current_user)
):

    return {
        "email": user["email"],
        "followers": user.get("followers", [])
    }@router.get("/my-followers")
async def my_followers(
    user = Depends(get_current_user)
):

    return {
        "email": user["email"],
        "followers": user.get("followers", [])
    }

@router.post("/save-post/{post_id}")
async def save_post_route(
    post_id: str,
    user = Depends(get_current_user)
):

    await save_post_service(
        user["email"],
        post_id
    )

    return {
        "message": "Post saved successfully"
    }

@router.get("/saved-posts")
async def saved_posts(
    user = Depends(get_current_user)
):

    latest_user = await get_user_by_email(
        user["email"]
    )

    return {
        "email": latest_user["email"],
        "saved_posts": latest_user.get(
            "saved_posts",
            []
        )
    }

@router.get("/search-users/{keyword}")
async def search_users_route(
    keyword: str
):

    users = await search_users(
        keyword
    )

    clean_users = []

    for user in users:

        clean_users.append({
            "email": user.get("email"),
            "role": user.get("role"),
            "name": user.get("name", ""),
            "bio": user.get("bio", "")
        })

    return {
        "results": clean_users
    }

@router.get("/user/{username}")
async def public_profile(
    username: str
):

    user = await get_user_by_username(
        username
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "username": user.get("username"),
        "email": user.get("email"),
        "role": user.get("role"),
        "bio": user.get("bio", ""),
        "followers": len(
            user.get("followers", [])
        ),
        "following": len(
            user.get("following", [])
        )
    }

@router.get("/user-posts/{username}")
async def user_posts(
    username: str
):

    posts = await get_posts_by_username(
        username
    )

    clean_posts = []

    for post in posts:

        clean_posts.append({
            "title": post.get("title"),
            "content": post.get("content"),
            "username": post.get("username")
        })

    return {
        "posts": clean_posts
    }

@router.get("/post-comments/{post_id}")
async def post_comments(
    post_id: str
):

    comments = await get_post_comments(
        post_id
    )

    return {
        "total_comments": len(comments),
        "comments": comments
    }

@router.get("/notifications")
async def notifications(
    user = Depends(get_current_user)
):

    latest_user = await get_user_by_email(
        user["email"]
    )

    return {
        "notifications":
        latest_user.get(
            "notifications",
            []
        )
    }

@router.post("/send-message")
async def send_message_route(
    data: MessageModel,
    user = Depends(get_current_user)
):

    await send_message(
        user["email"],
        data.receiver_email,
        data.message
    )

    return {
        "message": "Message sent successfully"
    }

@router.get("/my-messages")
async def my_messages(
    user = Depends(get_current_user)
):

    messages = await get_my_messages(
        user["email"]
    )

    clean_messages = []

    for msg in messages:

        clean_messages.append({
            "sender": msg.get("sender"),
            "message": msg.get("message")
        })

    return {
        "messages": clean_messages
    }
@router.get("/chat/{email}")
async def chat_history(
    email: str,
    user = Depends(get_current_user)
):

    messages = await get_chat_between_users(
        user["email"],
        email
    )

    clean_messages = []

    for msg in messages:

        clean_messages.append({
            "sender": msg.get("sender"),
            "receiver": msg.get("receiver"),
            "message": msg.get("message")
        })

    return {
        "chat": clean_messages
    }

@router.post("/set-online")
async def set_online(
    user = Depends(get_current_user)
):

    await set_user_online(
        user["email"]
    )

    return {
        "message": "You are now online"
    }

@router.get("/online-users")
async def online_users():

    users = await get_online_users()

    clean_users = []

    for user in users:

        clean_users.append({
            "email": user.get("email"),
            "role": user.get("role"),
            "username": user.get("username")
        })

    return {
        "online_users": clean_users
    }

@router.post("/upload-note")
async def upload_note_route(
    note: NoteModel,
    user = Depends(get_current_user)
):

    note_data = {
        "title": note.title,
        "description": note.description,
        "file_url": note.file_url,
        "uploaded_by": user["email"]
    }

    note_id = await upload_note(
        note_data
    )

    return {
        "message": "Note uploaded successfully",
        "note_id": note_id
    }

@router.get("/all-notes")
async def all_notes():

    notes = await get_all_notes()

    clean_notes = []

    for note in notes:

        clean_notes.append({
            "title": note.get("title"),
            "description": note.get("description"),
            "file_url": note.get("file_url"),
            "uploaded_by": note.get("uploaded_by")
        })

    return {
        "notes": clean_notes
    }

@router.post("/create-course")
async def create_course_route(
    course: CourseModel,
    user = Depends(get_current_user)
):

    course_data = {
        "title": course.title,
        "description": course.description,
        "category": course.category,
        "created_by": user["email"]
    }

    course_id = await create_course(
        course_data
    )

    return {
        "message": "Course created successfully",
        "course_id": course_id
    }

@router.get("/all-courses")
async def all_courses():

    courses = await get_all_courses()

    clean_courses = []

    for course in courses:

        clean_courses.append({
            "title": course.get("title"),
            "description": course.get("description"),
            "category": course.get("category"),
            "created_by": course.get("created_by")
        })

    return {
        "courses": clean_courses
    }
@router.post("/enroll-course/{course_id}")
async def enroll_course_route(
    course_id: str,
    user = Depends(get_current_user)
):

    await enroll_course(
        user["email"],
        course_id
    )

    return {
        "message": "Course enrolled successfully"
    }
@router.get("/my-enrollments")
async def my_enrollments(
    user = Depends(get_current_user)
):

    enrollments = await get_my_enrollments(
        user["email"]
    )

    return {
        "enrolled_courses": enrollments
    }

@router.post("/apply-admission")
async def apply_admission_route(
    data: AdmissionModel,
    user = Depends(get_current_user)
):

    admission_data = {
        "student_email": user["email"],
        "school_email": data.school_email,
        "full_name": data.full_name,
        "age": data.age,
        "class_name": data.class_name,
        "parent_email": data.parent_email,
        "parent_contact": data.parent_contact,
        "status": "pending"
    }

    admission_id = await apply_admission(
        admission_data
    )

    return {
        "message": "Admission applied successfully",
        "admission_id": admission_id
    }

@router.get("/school-applications")
async def school_applications(
    user = Depends(get_current_user)
):

    applications = await get_school_applications(
        user["email"]
    )

    clean_data = []

    for app in applications:

        clean_data.append({
            "student_email": app.get("student_email"),
            "full_name": app.get("full_name"),
            "age": app.get("age"),
            "class_name": app.get("class_name"),
            "parent_email": app.get("parent_email"),
            "parent_contact": app.get("parent_contact"),
            "status": app.get("status")
        })

    return {
        "applications": clean_data
    }

@router.post("/apply-school")
async def apply_school_route(
    data: TeacherApplicationModel,
    user = Depends(get_current_user)
):

    application_data = {
        "teacher_email": user["email"],
        "school_email": data.school_email,
        "full_name": data.full_name,
        "subject": data.subject,
        "experience": data.experience,
        "qualifications": data.qualifications,
        "area_of_interest": data.area_of_interest,
        "skills": data.skills,
        "certificates_url": data.certificates_url,
        "cv_url": data.cv_url,
        "status": "pending"
    }

    application_id = await apply_to_school(
        application_data
    )

    return {
        "message": "Applied to school successfully",
        "application_id": application_id
    }

@router.get("/teacher-applications")
async def teacher_applications(
    user = Depends(get_current_user)
):

    applications = await get_teacher_applications(
        user["email"]
    )

    clean_data = []

    for app in applications:

        clean_data.append({
            "teacher_email": app.get("teacher_email"),
            "full_name": app.get("full_name"),
            "subject": app.get("subject"),
            "experience": app.get("experience"),
            "qualifications": app.get("qualifications"),
            "area_of_interest": app.get("area_of_interest"),
            "skills": app.get("skills"),
            "certificates_url": app.get("certificates_url"),
            "cv_url": app.get("cv_url"),
            "status": app.get("status")
        })

    return {
        "applications": clean_data
    }
@router.post("/verify-user/{email}")
async def verify_user_route(
    email: str,
    user = Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only admin can verify users"
        )

    await verify_user(email)

    return {
        "message": f"{email} verified successfully"
    }

@router.post("/ban-user/{email}")
async def ban_user_route(
    email: str,
    user = Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only admin can ban users"
        )

    await ban_user(email)

    return {
        "message": f"{email} banned successfully"
    }

@router.delete("/delete-post/{post_id}")    
async def delete_bad_post(
    post_id: str,
    user = Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only admin can delete posts"
        )

    await delete_post(post_id)

    return {
        "message": "Post deleted successfully"
    }

@router.post("/upload-media")
async def upload_media(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):

    result = cloudinary.uploader.upload(
        file.file
    )

    return {
        "media_url": result["secure_url"]
    }

@router.get("/school/admissions")
async def view_school_admissions(
    user = Depends(get_current_user)
):

    applications = await get_school_applications(
        user["email"]
    )

    for app in applications:
        app["_id"] = str(app["_id"])

    return {
        "applications": applications
    }

@router.post("/school/admission/approve/{admission_id}")
async def approve_admission(
    admission_id: str,
    user = Depends(get_current_user)
):

    await update_admission_status(
        admission_id,
        "approved"
    )

    return {
        "message": "Admission approved"
    }

@router.post("/school/admission/reject/{admission_id}")
async def reject_admission(
    admission_id: str,
    user = Depends(get_current_user)
):

    await update_admission_status(
        admission_id,
        "rejected"
    )

    return {
        "message": "Admission rejected"
    }


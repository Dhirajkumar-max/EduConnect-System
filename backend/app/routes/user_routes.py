from fastapi import APIRouter, HTTPException

from app.models.user_model import User

from app.services.user_service import (
    create_user,
    get_user_by_email
)
from fastapi import Depends

from app.utils.auth_bearer import JWTBearer

from app.utils.hash import hash_password

router = APIRouter()


@router.post("/signup")
async def signup(user: User):

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
        "password": hashed_password
    }

    user_id = await create_user(user_data)

    return {
        "message": "User created successfully",
        "id": user_id
    }

@router.post("/login")
async def login(user: User):

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
            "email": user.email
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
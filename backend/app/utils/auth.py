from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import HTTPBearer

from jose import jwt, JWTError


SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

security = HTTPBearer()


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=403,
            detail="Invalid token"
        )


def get_current_user(credentials=Depends(security)):

    token = credentials.credentials

    return verify_token(token)


def teacher_only(user=Depends(get_current_user)):

    if user["role"] != "teacher":

        raise HTTPException(
            status_code=403,
            detail="Only teachers allowed"
        )

    return user

def student_only(user=Depends(get_current_user)):

    if user["role"] != "student":

        raise HTTPException(
            status_code=403,
            detail="Only students allowed"
        )

    return user
async def school_only(
    user = Depends(get_current_user)
):

    if user["role"] != "school":

        raise HTTPException(
            status_code=403,
            detail="Only schools allowed"
        )

    return user


async def admin_only(
    user = Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only admins allowed"
        )

    return user
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from jose import jwt, JWTError

from app.utils.jwt_handler import (
    SECRET_KEY,
    ALGORITHM
)


class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = (
            await super().__call__(request)
        )

        if credentials:

            token = credentials.credentials

            try:

                payload = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=[ALGORITHM]
                )

                return payload

            except JWTError as e:

                print(e)

                raise HTTPException(
                    status_code=403,
                    detail="Invalid token"
                )

        raise HTTPException(
            status_code=403,
            detail="Invalid authorization code"
        )
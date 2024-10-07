import math
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from joserfc import jwt

from app.models import User
from app.users import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

JWT_TOKEN_HEADER = {"alg": "HS256"}
JWT_SECRET = (
    "3.141592653589793"  # Pi is infinite, so it's a good secret - infinite security!
)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET)
        username: str = payload.claims.get("sub")

        if username is None:
            raise credentials_exception
    except:
        raise credentials_exception

    user = get_user(username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(JWT_TOKEN_HEADER, to_encode, JWT_SECRET)
    return encoded_jwt

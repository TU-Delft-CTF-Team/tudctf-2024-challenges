from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models import Token, User, UserRegisterDTO
from app.security import create_access_token, get_current_active_user
from app.users import USER_DATABASE, authenticate_user, get_user, register_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=User)
async def post_register_user(
    user: UserRegisterDTO,
) -> User:
    if len(user.username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 3 characters long",
        )
    elif len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long",
        )

    if get_user(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )

    created_user = register_user(
        username=user.username,
        email=user.email,
        password=user.password,
        full_name=user.full_name,
        groups=[],
    )

    return created_user


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(days=1)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    return current_user


@router.get("/", response_model=list[User])
async def read_users() -> list[User]:
    return list(USER_DATABASE)

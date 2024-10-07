from argon2 import PasswordHasher

from app.models import UserInDB

USER_DATABASE: list[UserInDB] = []

password_hasher = PasswordHasher()


def get_user(username: str) -> UserInDB | None:
    for user in USER_DATABASE:
        if user.username == username:
            return user
    return None


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if user is None:
        return None

    if not password_hasher.verify(user.hashed_password, password):
        return None

    return user


def register_user(
    username: str, email: str, password: str, full_name: str, groups: list[str]
) -> UserInDB:
    if get_user(username):
        raise ValueError("User already registered")

    user = UserInDB(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=password_hasher.hash(password),
        disabled=False,
        groups=groups,
    )
    USER_DATABASE.append(user)

    return user

from pydantic import BaseModel


class DetailResponse(BaseModel):
    detail: str


class Room(BaseModel):
    id: int
    name: str
    building: str
    booking_whitelist: list[str] | None = None
    capacity: int
    image: str
    contains_flag: bool


class RoomList(BaseModel):
    rooms: list[Room]


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False
    groups: list[str] = []


# This entity is only used by the client to send data to the server.
# Plaintext password is not stored in the database, and cannot be retrieved
# after registration.
class UserRegisterDTO(BaseModel):
    username: str
    email: str
    full_name: str
    password: str


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str

import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models import DetailResponse, Room, User
from app.rooms import RESERVATIONS, ROOMS
from app.security import get_current_active_user

router = APIRouter(
    prefix="/api/rooms", dependencies=[Depends(get_current_active_user)], tags=["rooms"]
)


@router.get("/reservations", response_model=dict[str, Room])
async def get_reservations(
    _: Annotated[User, Depends(get_current_active_user)]
) -> dict[str, Room]:
    return RESERVATIONS


@router.get("/", response_model=list[Room])
async def get_rooms() -> list[Room]:
    return ROOMS


@router.get("/{room_id}", response_model=Room)
async def get_room(room_id: int) -> Room:
    for room in ROOMS:
        if room.id == room_id:
            return room
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")


@router.post("/{room_id}", response_model=DetailResponse)
async def book_room(
    room_id: int, current_user: Annotated[User, Depends(get_current_active_user)]
) -> DetailResponse:
    # Check if the user already has a reservation
    if current_user.username in RESERVATIONS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has a reservation",
        )

    # Check if the room is already reserved
    if room_id in RESERVATIONS.items():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Room already reserved"
        )

    for room in ROOMS:
        if room.id != room_id:
            continue

        # Check if the user is allowed to book the room
        if (
            room.booking_whitelist
            and len(set(current_user.groups).intersection(room.booking_whitelist)) == 0
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not allowed to book the room",
            )

        # Reserve the room
        RESERVATIONS[current_user.username] = room
        return DetailResponse(detail="Room reserved")

    raise HTTPException(status_code=404, detail="Room not found")


@router.delete("/{room_id}", response_model=DetailResponse)
async def cancel_room(
    room_id: int, current_user: Annotated[User, Depends(get_current_active_user)]
) -> DetailResponse:
    if (
        current_user.username not in RESERVATIONS
        or RESERVATIONS[current_user.username].id != room_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not reserved"
        )

    del RESERVATIONS[current_user.username]

    return DetailResponse(detail="Room reservation canceled")


@router.post("/use/{room_id}", response_model=DetailResponse)
async def use_room(
    room_id: int, current_user: Annotated[User, Depends(get_current_active_user)]
) -> DetailResponse:
    if (
        current_user.username not in RESERVATIONS
        or RESERVATIONS[current_user.username].id != room_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not reserved"
        )

    room = RESERVATIONS[current_user.username]
    if room.contains_flag:
        # If the user uses the room with the flag, return the flag
        return DetailResponse(detail=os.getenv("FLAG", "TUDCTF{THIS_IS_A_FAKE_FLAG}"))
    else:
        return DetailResponse(detail="Lots of interesting things, but no flag...")

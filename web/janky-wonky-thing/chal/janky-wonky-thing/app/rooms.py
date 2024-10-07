from pathlib import Path

from app.models import Room, RoomList

# List of all available rooms
ROOMS: list[Room] = []

# Dictionary of room reservations
# Key: username
# Value: reserved room
RESERVATIONS: dict[str, Room] = {}


def load_rooms(from_file: Path):
    global ROOMS

    with open(from_file) as file:
        ROOMS.extend(RoomList.model_validate_json(file.read()).rooms)

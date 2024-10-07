async function bookRoom(room_id) {
  try {
    const response = await fetch(`/api/rooms/${room_id}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("janky-token")}`,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail);
    }

    window.location.href = `/?info=${encodeURIComponent(data.detail)}`;
  } catch (error) {
    console.log(error);
    alert(error.message);
    return;
  }
}

async function cancelRoom(room_id) {
  try {
    const response = await fetch(`/api/rooms/${room_id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("janky-token")}`,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail);
    }

    window.location.href = `/?info=${encodeURIComponent(data.detail)}`;
  } catch (error) {
    console.log(error);
    alert(error.message);
    return;
  }
}

async function getCurrentBookings() {
  const response = await fetch("/api/rooms/reservations", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("janky-token")}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail);
  }

  return data;
}

async function getCurrentUser() {
  const response = await fetch("/api/users/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("janky-token")}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail);
  }

  return data;
}

async function useRoom(room_id) {
  try {
    const response = await fetch(`/api/rooms/use/${room_id}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("janky-token")}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail);
    }

    window.location.href = `/?info=${encodeURIComponent(data.detail)}`;
  } catch (error) {
    console.log(error);
    alert(error.message);
    return;
  }
}

async function loadRooms() {
  const ROOMS_LIST = document.getElementById("room-list");
  const ROOM_TEMPLATE = document.getElementById("room-template");

  try {
    const user = await getCurrentUser();

    document.getElementById("user-display").textContent = `Current user: ${user.username}`;

    const reservations = await getCurrentBookings();

    const response = await fetch("/api/rooms/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("janky-token")}`,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail);
    }

    for (const room of data) {
      const ROOM = ROOM_TEMPLATE.content.cloneNode(true);

      ROOM.querySelector(".room-name").textContent = room.name;
      ROOM.querySelector(".building-name").textContent = room.building;
      ROOM.querySelector(".room-capacity").textContent = room.capacity;
      ROOM.querySelector(".room-img-thumbnail").src = room.image;
      ROOM.querySelector(".room-img-thumbnail").alt = room.name;

      const restrictions_text = room.booking_whitelist
        ? `Only following: ${room.booking_whitelist.join(", ")}`
        : "None";
      ROOM.querySelector(".room-restrictions").textContent = restrictions_text;

      let isRoomReserved = false;
      let reserved_by_this_user = false;
      for (const reserved_room of Object.values(reservations)) {
        if (reserved_room.id == room.id) {
          isRoomReserved = true;
          reserved_by_this_user =
            reservations.hasOwnProperty(user.username) &&
            reservations[user.username].id == reserved_room.id;
          break;
        }
      }

      if (!isRoomReserved) {
        ROOM.querySelector(".room-book-button").addEventListener(
          "click",
          () => {
            bookRoom(room.id);
          }
        );
        ROOM.querySelector(".room-use-button").style.display = "none";
      } else if (isRoomReserved && reserved_by_this_user) {
        ROOM.querySelector(".room-book-button").textContent = "Cancel booking";
        ROOM.querySelector(".room-book-button").addEventListener(
          "click",
          () => {
            cancelRoom(room.id);
          }
        );
        ROOM.querySelector(".room-use-button").style.display = "block";
        ROOM.querySelector(".room-use-button").addEventListener("click", () => {
          useRoom(room.id);
        });
      } else {
        ROOM.querySelector(".room-reserved-by-anoter").style.display = "block";
        ROOM.querySelector(".room-book-button").style.display = "none";
        ROOM.querySelector(".room-use-button").style.display = "none";
      }

      ROOMS_LIST.appendChild(ROOM);
    }

    console.log(data);
  } catch (error) {
    console.log(error);
    alert(error.message);
    return;
  }
}

document.addEventListener("DOMContentLoaded", loadRooms);

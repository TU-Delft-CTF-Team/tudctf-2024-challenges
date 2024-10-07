async function loadUsers() {
  const USER_LIST_ELEMENT = document.getElementById("user-list");

  try {
    const resp = await fetch("/api/users/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("janky-token")}`,
      },
    });

    const data = await resp.json();
    if (!resp.ok) {
      throw new Error(data.detail);
    }

    for (const user of data) {
      const USER_CONTAINER = document.createElement("li");
      USER_CONTAINER.classList.add("list-group-item");
      USER_CONTAINER.innerText = `Username: ${user.username} (${user.full_name})`;

      USER_LIST_ELEMENT.appendChild(USER_CONTAINER);
    }
  } catch (error) {
    console.log(error);
    alert(error.message);
    return;
  }
}

document.addEventListener("DOMContentLoaded", loadUsers);

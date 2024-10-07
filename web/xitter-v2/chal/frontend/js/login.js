document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const inputUsername = document.getElementById("input-username");
  const inputPassword = document.getElementById("input-password");

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const username = inputUsername.value;
    const password = inputPassword.value;

    fetch(`${window.remote_url}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Failed to log in");
        }
      })
      .then((data) => {
        localStorage.setItem("token", data.token);
        window.location.href = "/index.html";
      })
      .catch((error) => {
        console.error(error);
        window.location.href = "/login.html?error=Failed to log in";
      });
  });
});

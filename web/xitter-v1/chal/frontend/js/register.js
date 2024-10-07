document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const inputUsername = document.getElementById("input-username");
  const inputPassword = document.getElementById("input-password");

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const username = inputUsername.value;
    const password = inputPassword.value;

    fetch(`${window.remote_url}/api/auth/register`, {
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
          window.location.href = "/login.html?info=Successfully registered";
        } else {
          window.location.href = "/register.html?error=Failed to register";
        }
      })
      .catch((error) => {
        console.error(error);
        window.location.href = "/register.html?error=Failed to register";
      });
  });
});

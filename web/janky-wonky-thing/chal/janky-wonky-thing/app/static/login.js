async function loginMain() {
  const LOGIN_FORM = document.getElementById("login-form");

  LOGIN_FORM.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(LOGIN_FORM);

    const USERNAME = formData.get("inputUsername");
    const PASSWORD = formData.get("inputPassword");

    const body = new FormData();
    body.set("username", USERNAME);
    body.set("password", PASSWORD);

    try {
      const response = await fetch("/api/users/login", {
        method: "POST",
        body,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail);
      }

      localStorage.setItem("janky-token", data.access_token);
      window.location.href = "/";
    } catch (error) {
      window.location.href = `/login?error=${encodeURIComponent(
        error.message
      )}`;
    }
  });
}

document.addEventListener("DOMContentLoaded", loginMain);

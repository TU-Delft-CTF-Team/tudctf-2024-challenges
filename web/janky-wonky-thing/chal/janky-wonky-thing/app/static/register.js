async function registrationMain() {
  const REGISTER_FORM = document.getElementById("register-form");

  REGISTER_FORM.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(REGISTER_FORM);

    const PASSWORD = formData.get("inputPassword");
    const CONFIRM_PASSWORD = formData.get("inputConfirmPassword");
    const USERNAME = formData.get("inputUsername");
    const EMAIL = formData.get("inputEmail");
    const FULLNAME = formData.get("inputFullName");

    try {
      if (PASSWORD !== CONFIRM_PASSWORD) {
        throw new Error("Passwords do not match");
      } else if (PASSWORD.length < 8) {
        throw new Error("Password must be at least 8 characters long");
      } else if (USERNAME.length < 3) {
        throw new Error("Username must be at least 3 characters long");
      } else if (FULLNAME.length < 1) {
        throw new Error("Full name must not be empty");
      } else if (!EMAIL.includes("@")) {
        throw new Error("Invalid email address");
      }
    } catch (error) {
      window.location.href = `/register?error=${encodeURIComponent(
        error.message
      )}`;
      return;
    }

    const body = {
      username: USERNAME,
      password: PASSWORD,
      email: EMAIL,
      full_name: FULLNAME,
    };

    try {
      const response = await fetch("/api/users/register", {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const response_json = await response.json();

      if (!response.ok) {
        throw new Error(response_json.detail);
      }

      window.location.href = `/login?info=${encodeURIComponent(
        "Registration successful! Please log in."
      )}`;
    } catch (error) {
      console.log(error);
      window.location.href = `/register?error=${encodeURIComponent(
        error.message
      )}`;
    }
  });
}

document.addEventListener("DOMContentLoaded", registrationMain);

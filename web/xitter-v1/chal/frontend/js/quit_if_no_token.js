if (!localStorage.getItem("token")) {
  window.location.href = "/login.html";
}

window.auth_token = localStorage.getItem("token");
window.auth_token_header = `Bearer ${window.auth_token}`;
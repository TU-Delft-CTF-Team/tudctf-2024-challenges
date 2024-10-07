const token = localStorage.getItem("janky-token");
if (!token) {
  window.location.href = "/login";
}

window.auth_token = token;

fetch("/api/users/me", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
})
  .then((response) => {
    if (response.status < 200 || response.status >= 300) {
      window.location.href = "/login";
    }
  })
  .catch(() => {
    window.location.href = "/login";
  });

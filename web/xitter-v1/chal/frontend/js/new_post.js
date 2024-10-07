document.addEventListener("DOMContentLoaded", () => {
  const postForm = document.getElementById("post-form");
  const inputContents = document.getElementById("postContentsInput");
  const inputPrivate = document.getElementById("privatePostInput");

  postForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const contents = inputContents.value;
    const isPrivate = inputPrivate.checked;

    fetch(`${window.remote_url}/api/post/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: window.auth_token_header,
      },
      body: JSON.stringify({
        content: contents,
        isPrivate,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Failed to create a xeet");
        }
      })
      .then((_) => {
        window.location.href = "/index.html";
      })
      .catch((error) => {
        console.error(error);
        window.location.href = "/new_post.html?error=Failed to create a xeet";
      });
  });
});

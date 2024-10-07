async function main() {
  let posts_raw = await fetch(`${window.remote_url}/api/post/latest`, {
    headers: {
      Authorization: window.auth_token_header,
    },
  });

  let posts = await posts_raw.json();

  const postTemplate = document.getElementById("xitter-post");
  for (const post of posts) {
    const postElement = postTemplate.content.cloneNode(true);

    const postContents = postElement.querySelector(".post-contents");
    postContents.textContent = post.content;

    const authorLink = postElement.querySelector(".author-link");
    authorLink.href = `/user.html?id=${post.authorId}`;
    authorLink.textContent = post.authorUsername;

    if (post.isPrivate) {
      const privateBadge = postElement.querySelector(".private-tag");
      privateBadge.style.display = "inline";
    }

    document.getElementById("post-container").appendChild(postElement);
  }
}

document.addEventListener("DOMContentLoaded", main);

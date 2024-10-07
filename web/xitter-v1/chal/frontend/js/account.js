async function main() {
  try {
    let user_raw = await fetch(`${window.remote_url}/api/user/me`, {
      headers: {
        Authorization: window.auth_token_header,
      },
    });

    if (user_raw.status > 299) {
      throw new Error("Invalid user");
    }
    let user = await user_raw.json();

    document.getElementById("num-followers").textContent =
      user.followers.length;
    document.getElementById("num-following").textContent =
      user.following.length;

    let user_posts = await fetch(
      `${window.remote_url}/api/post/user/${user.id}`,
      {
        headers: {
          Authorization: window.auth_token_header,
        },
      }
    );
    let posts = await user_posts.json();
    const postTemplate = document.getElementById("xitter-post");
    for (const post of posts) {
      const postElement = postTemplate.content.cloneNode(true);

      const postContents = postElement.querySelector(".post-contents");
      postContents.textContent = post.content;

      const postAuthor = postElement.querySelector(".author-link");
      postAuthor.textContent = post.authorUsername;
      postAuthor.href = `/user.html?id=${post.authorId}`;

      if (post.isPrivate) {
        const privateBadge = postElement.querySelector(".private-tag");
        privateBadge.style.display = "inline";
      }

      document.getElementById("post-container").appendChild(postElement);
    }
    document.getElementById("num-posts").textContent = posts.length;
  } catch (e) {
    console.error(e);
    window.location.href = "/login.html";
  }
}

document.addEventListener("DOMContentLoaded", main);

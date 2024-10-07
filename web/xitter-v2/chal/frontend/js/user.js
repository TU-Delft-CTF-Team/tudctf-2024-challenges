let is_following = false;

function doesFollowerExist(followers, id) {
  for (const follower of followers) {
    if (follower.id === id) {
      return true;
    }
  }
  return false;
}

async function main() {
  let urlParams = new URLSearchParams(window.location.search);
  let id = urlParams.get("id");
  if (!id) {
    window.location.href = "/index.html";
    return;
  }

  try {
    let user_raw = await fetch(`${window.remote_url}/api/user/overview/${id}`, {
      headers: {
        Authorization: window.auth_token_header,
      },
    });

    if (user_raw.status > 299) {
      throw new Error("Invalid user");
    }
    let user = await user_raw.json();

    let my_user_raw = await fetch(`${window.remote_url}/api/user/me`, {
      headers: {
        Authorization: window.auth_token_header,
      },
    });

    if (my_user_raw.status > 299) {
      throw new Error("Invalid user");
    }
    let my_user = await my_user_raw.json();

    if (my_user.id === user.id) {
      window.location.href = "/account.html";
      return;
    }

    console.log(my_user);
    if (doesFollowerExist(my_user.following, user.id)) {
      document.getElementById("follow-button").textContent = "Unfollow";
      is_following = true;
    } else {
      document.getElementById("follow-button").textContent = "Follow";
      is_following = false;
    }

    document
      .getElementById("follow-button")
      .addEventListener("click", async () => {
        if (is_following) {
          let unfollow = await fetch(
            `${window.remote_url}/api/user/follow/${user.id}`,
            {
              method: "DELETE",
              headers: {
                Authorization: window.auth_token_header,
              },
            }
          );
          if (unfollow.status > 299) {
            throw new Error("Invalid user");
          }
          document.getElementById("follow-button").textContent = "Follow";
          is_following = false;
        } else {
          let follow = await fetch(
            `${window.remote_url}/api/user/follow/${user.id}`,
            {
              method: "POST",
              headers: {
                Authorization: window.auth_token_header,
              },
            }
          );
          if (follow.status > 299) {
            throw new Error("Invalid user");
          }
          document.getElementById("follow-button").textContent = "Unfollow";
          is_following = true;
        }
      });

    document.getElementById("username-heading").textContent = user.username;
    document.getElementById("num-following").textContent = user.following;
    document.getElementById("num-followers").textContent = user.followers;

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

      const postAuthor = postElement.querySelector(".post-author");
      postAuthor.textContent = post.authorUsername;

      document.getElementById("post-container").appendChild(postElement);
    }
    document.getElementById("num-posts").textContent = posts.length;
  } catch (e) {
    window.location.href = "/login.html";
  }
}

document.addEventListener("DOMContentLoaded", main);

import os
import secrets
import time

import requests

REMOTE = "http://127.0.0.1:8080"
ADMIN_USER = "admin"
ADMIN_PASSWORD = secrets.token_urlsafe(10)
FLAG = os.getenv("FLAG") or "TUDCTF{THIS_IS_A_TEST_FLAG}"

# Verify that the server is up
while True:
    try:
        r = requests.get(f"{REMOTE}/api/health")
        break
    except:
        time.sleep(1)

r = requests.post(
    f"{REMOTE}/api/auth/register",
    json={"username": ADMIN_USER, "password": ADMIN_PASSWORD},
)
r.raise_for_status()

print(f"Admin user created")

r = requests.post(
    f"{REMOTE}/api/auth/login",
    json={"username": ADMIN_USER, "password": ADMIN_PASSWORD},
)
r.raise_for_status()

print(f"Login successful")

token = r.json()["token"]

auth_header = {"Authorization": f"Bearer {token}"}

r = requests.post(
    f"{REMOTE}/api/post/create",
    headers=auth_header,
    json={"content": FLAG, "isPrivate": True},
)
r.raise_for_status()

print(f"Flag post created")

r = requests.post(
    f"{REMOTE}/api/post/create",
    headers=auth_header,
    json={
        "content": "This is a public post. I definitely didn't use a private post to store a flag.",
        "isPrivate": False,
    },
)
r.raise_for_status()

print(f"Public post created")

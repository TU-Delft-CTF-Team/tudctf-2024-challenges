from flask import Flask, render_template, jsonify

import json

import os

from secret import decrypt

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Welcome Admin!</h1><br><p>Use /api/user/user_id or /api/export to inspect user data or export the encrypted data.</p>"


@app.route("/api/user/<user_id>")
def get_user(user_id):
    user_file = f"{user_id}.json"
    if user_file not in os.listdir("users"):
        return "User ID not found"

    with open(f"users/{user_file}", "r") as file:
        user_data = json.load(file)

    for key in user_data:
        user_data[key] = decrypt(user_data[key])

    return jsonify(user_data)


def user_file_to_json(user_path):
    with open(user_path, "r") as file:
        return json.load(file)


@app.route("/api/export")
def export():
    json_data = [
        user_file_to_json(f"users/{user_id}") for user_id in os.listdir("users")
    ]
    return render_template("list.html", json_data=json_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)

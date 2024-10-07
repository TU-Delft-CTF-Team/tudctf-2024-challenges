from flask import Flask, request, send_file, redirect, render_template

from selenium.webdriver import Chrome, ChromeOptions

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from PIL import Image

import numpy as np

import uuid

import time

import threading

import os

import shutil

import json

from secret import decrypt, encrypt, FLAG

plt.switch_backend("Agg")

app = Flask(__name__)


@app.route("/")
def hello_world():
    return send_file("static/index.html")


@app.route("/pricing")
def pricing():
    return send_file("static/pricing.html")


@app.route("/buy", methods=["GET", "POST"])
def buy():
    if request.method == "GET":
        return send_file("static/buy.html")

    user_data = {}
    user_data["id"] = request.json["id"]
    user_data["name"] = request.json["name"]
    user_data["subscription"] = request.json["subscription"]
    user_data["bank_number"] = request.json["bank_number"]

    user_id = decrypt(user_data["id"])
    user_file = f"users/{user_id}.json"
    with open(user_file, "w") as file:
        json.dump(user_data, file)

    return redirect("/")


@app.route("/robots.txt")
def robots():
    return send_file("static/robots.txt")


@app.route("/security.txt")
def security():
    return send_file("static/security.txt")


@app.route("/src")
def src():
    return send_file("app.py")


@app.route("/screenshot", methods=["GET", "POST"])
def screenshot():
    if request.method == "GET":
        return send_file("static/screenshot.html")

    url_to_request = request.form["url"]
    if not url_to_request.startswith("http://") and not url_to_request.startswith(
        "https://"
    ):
        url_to_request = "http://" + request.form["url"]

    filename = str(uuid.uuid4())
    filepath = "screenshots/" + filename

    css_path = "static/shreksy.css"

    thread = threading.Thread(
        target=take_screenshot, args=[url_to_request, filepath, css_path]
    )
    thread.start()
    return redirect(f"/view/{filename}")


@app.route("/view/<screen_id>")
def view(screen_id):
    try:
        uuid.UUID(screen_id, version=4)
    except:
        message = "That's not a UUID!"
        return render_template("message.html", message=message)

    image_name = str(screen_id) + ".pdf"
    if image_name in os.listdir("screenshots"):
        return send_file("screenshots/" + image_name)
    else:
        message = "Refresh to download your screenshot when it is ready. Be patient! This can take 10 seconds."
        return render_template("message.html", message=message)


def take_screenshot(url, name=None, custom_stylesheet=None, width=1920, height=1080):
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument(f"--window-size={width},{height}")

    browser = Chrome(options)

    browser.get(url)

    if custom_stylesheet:
        custom_css = open(custom_stylesheet, "r").read()
        script = f"""
        var style = document.createElement('style');
        style.type = 'text/css';
        style.appendChild(document.createTextNode(`{custom_css}`));
        document.head.appendChild(style);
        """
        browser.execute_script(script)

    time.sleep(1)

    browser.save_screenshot(name + ".png")

    browser.quit()

    convert_png_to_pdf_with_watermark(name + ".png", name + ".pdf")


def convert_png_to_pdf_with_watermark(
    input_image_path, output_pdf_path, watermark_image_path="static/shrek.png"
):
    watermark_text = "Shreksy™\npreview"

    image = mpimg.imread(input_image_path)
    image_height, image_width, _ = image.shape

    _, ax = plt.subplots(figsize=(image_width / 100, image_height / 100), dpi=100)

    ax.imshow(image)

    font_size = int(image_width / 15)
    ax.text(
        image_width / 2,
        150,
        watermark_text,
        color=(0.37, 0.38, 0.05, 1),
        fontsize=font_size,
        ha="center",
        va="top",
        fontweight="black",
        fontfamily="sans-serif",
    )

    watermark_image = Image.open(watermark_image_path).convert("RGBA")
    base_width = int(image_width / 8)
    w_percent = base_width / float(watermark_image.size[0])
    h_size = int((float(watermark_image.size[1]) * float(w_percent)))
    watermark_image = watermark_image.resize((base_width, h_size))

    watermark_np = np.array(watermark_image) / 255.0

    bottom_left_position = (200, image_height - h_size - 360)
    bottom_right_position = (
        image_width - base_width - 200,
        image_height - h_size - 360,
    )

    ab_bottom_left = AnnotationBbox(
        OffsetImage(watermark_np, zoom=1),
        (
            bottom_left_position[0] + base_width / 2,
            bottom_left_position[1] + h_size / 2,
        ),
        frameon=False,
    )
    ax.add_artist(ab_bottom_left)
    ab_bottom_right = AnnotationBbox(
        OffsetImage(watermark_np, zoom=1),
        (
            bottom_right_position[0] + base_width / 2,
            bottom_right_position[1] + h_size / 2,
        ),
        frameon=False,
    )
    ax.add_artist(ab_bottom_right)
    ax.axis("off")

    plt.savefig(output_pdf_path, bbox_inches="tight", pad_inches=0)
    plt.close()


def clear_or_create_directory(directory_path):
    # Creates a directory or clears it if it exists
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)

    os.makedirs(directory_path)


if __name__ == "__main__":
    clear_or_create_directory("users")
    clear_or_create_directory("screenshots")

    flag_user_id = os.urandom(8).hex()
    flag_user_file = f"users/{flag_user_id}.json"
    flag_user_data = {
        "id": encrypt(flag_user_id),
        "name": encrypt("Flaggy McFlagalot"),
        "subscription": encrypt("Unlimited Access"),
        "bank_number": encrypt(FLAG),
    }
    with open(flag_user_file, "w") as file:
        json.dump(flag_user_data, file)

    normal_user_id = os.urandom(8).hex()
    normal_user_file = f"users/{normal_user_id}.json"
    normal_user_data = {
        "id": encrypt(normal_user_id),
        "name": encrypt("Skibidy Toilet"),
        "subscription": encrypt("Monthly"),
        "bank_number": encrypt("123456789abcdef"),
    }
    with open(normal_user_file, "w") as file:
        json.dump(normal_user_data, file)

    app.run(host="0.0.0.0", port=5005)

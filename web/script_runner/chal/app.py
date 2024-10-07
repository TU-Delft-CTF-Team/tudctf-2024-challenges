from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import subprocess
import os
import utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=["POST"])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return render_template('index.html')

    file_path = os.path.join('uploads', secure_filename(uploaded_file.filename))
    uploaded_file.save(file_path)

    file_hash = utils.get_secure_hash(file_path)
    if not utils.is_allowed(file_hash):
        return render_template('index.html', output="Script not allowed!")

    output = utils.execute_script(file_path)

    return render_template('index.html', output=output)

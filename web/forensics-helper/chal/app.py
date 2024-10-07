from flask import Flask, render_template, redirect, url_for, request, flash
import os
import secrets
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4'}

@app.route('/')
def index():
    return render_template('index.html')

def get_exif_data(sanitized_filepath):
    result = subprocess.run(' '.join(['exiftool', sanitized_filepath]), capture_output=True, shell=True, text=True)
    exif_data = result.stdout.splitlines()
    print(exif_data)
    try:
        exif_data_parsed = [(tag, value) for tag, value in (t.split(': ', 1) for t in exif_data)]
    except Exception as ex:
        flash(f'Something went wrong while parsing exiftool output: {ex}')
        exif_data_parsed = []
    return exif_data_parsed


@app.route('/', methods=['POST'])
def upload():    
    if 'file' not in request.files or not request.files['file'] or request.files['file'].filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    filename = request.files['file'].filename
    
    if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        flash(f'Only the following extensions are allowed: {ALLOWED_EXTENSIONS}')
        return redirect(url_for('index'))
    
    sanitized_filename = os.path.normpath(filename)
    sanitized_path = os.path.join(UPLOAD_FOLDER, sanitized_filename)
    
    request.files['file'].save(sanitized_path)
    exif_data = get_exif_data(f'"{UPLOAD_FOLDER}/{sanitized_filename}"')
    os.remove(sanitized_path)
    
    return render_template('index.html', exif_data=exif_data, filename=sanitized_filename)

if __name__ == '__main__':
    app.run()

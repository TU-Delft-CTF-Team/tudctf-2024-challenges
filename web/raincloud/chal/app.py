from flask import Flask, render_template, redirect, url_for, flash, request, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///:memory:'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String(150), primary_key=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
db.init_app(app)

def seed_database():
    if User.query.count() == 0:
        admin_user = User(username='admin', password=generate_password_hash(secrets.token_hex(16)))
        db.session.add(admin_user)
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
        
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html')
    
    session['username'] = username
    flash('Login successful', 'success')
    return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method != 'POST':
        return render_template('register.html')
    
    username = request.form['username']
    password = request.form['password']
    
    if not username or any(c not in string.ascii_lowercase for c in username):
        flash('Username must consist of between 1 and 10 lowecase characters', 'danger')
        return render_template('register.html')
        
    
    if User.query.filter_by(username=username).first():
        flash('User already exists', 'danger')
        return render_template('register.html')
    
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    os.mkdir(f"{app.config['UPLOAD_FOLDER']}/{username}")
    
    flash('Your account has been created! You can now log in', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    username = session['username']
    
    files = os.listdir(f"{app.config['UPLOAD_FOLDER']}/{session['username']}")
    
    return render_template('dashboard.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        flash('You are not logged in', 'danger')
        return redirect(url_for('login'))
    
    if 'file' not in request.files or not request.files['file'] or request.files['file'].filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('dashboard'))
    
    request.files['file'].save(f"{app.config['UPLOAD_FOLDER']}/{session['username']}/{request.files['file'].filename}")
    flash('File successfully uploaded', 'success')
    return redirect(url_for('dashboard'))

@app.route('/download')
def download():
    if 'username' not in session:
        flash('You are not logged in', 'danger')
        return redirect(url_for('login'))
    
    user = request.args.get('user')
    filename = request.args.get('filename')

    if not user or not filename or session['username'] != user:
        flash('You cannot access this file!', 'danger')
        return redirect(url_for('dashboard'))
    
    return send_file(f"{app.config['UPLOAD_FOLDER']}/{user}/{filename}")

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, redirect, url_for, flash, request, g
import base64
import secrets
import os
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

users = {
    'admin': {
        'password': secrets.token_hex(16),
        'is_admin': True
    },
    'guest': {
        'password': 'guest',
        'is_admin': False
    }
}

def encrypt(s):
    # military-grade encryption 😤
    return base64.b64encode(s.encode()).decode()
    
def decrypt(s):
    return base64.b64decode(s.encode()).decode()

@app.before_request
def decrypt_user():
    if 'user' in request.cookies and request.cookies.get('user'):
        g.username = decrypt(request.cookies.get('user'))
    else:
        g.username = None
    

@app.route('/')
def index():
    if not g.username:
        flag = 'Please log in!'
    elif users[g.username]['is_admin'] == True:
        flag = os.getenv('FLAG')
    else:
        flag = f'Hi, {g.username}! You are unfortunately not an admin.'
    return render_template('index.html', username=g.username, flag=flag)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
        
    username = request.form['username']
    password = request.form['password']
    
    if username not in users or users[username]['password'] != password:
        flash('Invalid username or password!', 'danger')
        return render_template('login.html')
    
    flash('Login successful', 'success')
    response = redirect(url_for('index'))
    response.set_cookie('user', encrypt(username))
    return response

@app.route('/logout')
def logout():
    flash('You have been logged out.', 'success')
    response = redirect(url_for('index'))
    response.set_cookie('user', '')
    return response

if __name__ == '__main__':
    app.run()

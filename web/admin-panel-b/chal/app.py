from flask import Flask, render_template, redirect, url_for, flash, request, session
import secrets
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/')
def index():
    if 'username' not in session:
        flag = 'Please log in!'
    elif session['is_admin'] == True:
        flag = os.getenv('FLAG')
    else:
        flag = f'Hi, {session["username"]}! You are unfortunately not an admin.'
    return render_template('index.html', username=session.get('username', None), flag=flag)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
        
    username = request.form['username']
    password = request.form['password']
    
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    result = cur.fetchone()
    
    if not result:
        flash('Invalid username or password!', 'danger')
        return render_template('login.html')
    
    flash('Login successful', 'success')
    session['username'] = result[1]
    session['is_admin'] = result[3]
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    flash('You have been logged out.', 'success')
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

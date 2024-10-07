from flask import Flask, render_template, Response
import os
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/something', methods=['OPTIONS'])
def something():
    resp = Response("there's nothing here I promise") 
    resp.headers['X-Something'] = os.environ['FLAG']
    return resp

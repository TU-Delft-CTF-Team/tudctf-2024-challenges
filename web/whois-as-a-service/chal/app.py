from flask import Flask, render_template, request
import secrets
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Hint: the flag is under /flag.txt (see the Dockerfile)

@app.route('/')
def index():
    return render_template('index.html')

def run_whois(whois):
    result = subprocess.run(f'whois {whois}', capture_output=True, shell=True, text=True)
    result = result.stdout + result.stderr
    return result

@app.route('/', methods=['POST'])
def upload():
    whois = request.form.get('whois', '')

    whois_result = run_whois(whois) if whois else ''

    return render_template('index.html', whois=whois, data=whois_result)

if __name__ == '__main__':
    app.run()

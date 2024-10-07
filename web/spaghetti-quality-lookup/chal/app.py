from flask import Flask, render_template, request, flash
import secrets
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/')
def index():
    if 'query' not in request.args:
        return render_template('index.html')
    
    query = request.args.get('query')
    
    q = f"SELECT spaghetti, qualities FROM spaghetti_types WHERE spaghetti LIKE '%{query}%'"
    
    try:
        con = sqlite3.connect("spaghetti.db")
        cur = con.cursor()
        cur.execute(q)
        results = cur.fetchall()
        return render_template('index.html', results=results, query=query)
    except:
        flash(f'An error occurred while executing query: {q}')
        return render_template('index.html', query=query)

if __name__ == '__main__':
    app.run()

import sqlite3
import secrets

con = sqlite3.connect("users.db")
cur = con.cursor()

cur.execute("CREATE TABLE users(id, username, password, is_admin)")
cur.execute(f"""
            INSERT INTO users VALUES
            (1, 'admin', '{secrets.token_hex(16)}', true),
            (2, 'guest', 'guest', false)
            """)
con.commit()

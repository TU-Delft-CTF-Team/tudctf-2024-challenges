#!/bin/sh
python3 init_db.py
gunicorn app:app -b 0.0.0.0:8080

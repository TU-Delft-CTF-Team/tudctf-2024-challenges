#!/bin/sh
echo "$FLAG" > /app/uploads/admin/flag.txt
gunicorn app:app -b 0.0.0.0:8080

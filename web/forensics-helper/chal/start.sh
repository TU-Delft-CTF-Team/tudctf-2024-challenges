#!/bin/sh
echo "$FLAG" > /flag.txt
gunicorn app:app -b 0.0.0.0:8080

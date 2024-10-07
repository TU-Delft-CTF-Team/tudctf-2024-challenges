#!/bin/sh
echo "$FLAG" > /flag.txt
gunicorn app:app -w 4 -b 0.0.0.0:8080

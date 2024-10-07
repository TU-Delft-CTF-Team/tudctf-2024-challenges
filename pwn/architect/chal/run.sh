#!/bin/sh

python3 server.py > /dev/null 2>&1 &
socat tcp-listen:1337,reuseaddr,fork exec:/app/architect

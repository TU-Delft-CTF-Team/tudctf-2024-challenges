#!/bin/sh

docker build -t tudctf/printing .
docker run -d -p 5000:5000 --privileged tudctf/printing
# connect to localhost:5000 to access the challenge
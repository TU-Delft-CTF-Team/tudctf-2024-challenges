#!/bin/sh

docker build -t tudctf/pivot .
docker run -d -p 5000:5000 --privileged tudctf/pivot
# connect to localhost:5000 to access the challenge
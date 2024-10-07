#!/bin/sh

docker build -t tudctf/flowing_over .
docker run -d -p 5000:5000 --privileged tudctf/flowing_over
# connect to localhost:5000 to access the challenge
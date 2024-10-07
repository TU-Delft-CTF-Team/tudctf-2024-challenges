#!/bin/sh

docker build -t tudctf/exotic-cookbook .
docker run -p 5000:5000 --privileged tudctf/exotic-cookbook
# connect to localhost:5000 to access the challenge


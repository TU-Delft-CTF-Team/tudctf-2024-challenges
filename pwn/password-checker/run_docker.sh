#!/bin/sh

docker build -t tudctf/password-checker .
docker run -p 5000:5000 --privileged tudctf/password-checker
# connect to localhost:5000 to access the challenge

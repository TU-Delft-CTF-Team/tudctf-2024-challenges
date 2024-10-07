#!/bin/sh

docker build -t tudctf/rsa-cca .
docker run -p 5000:5000 --privileged tudctf/rsa-cca
# connect to localhost:5000 to access the challenge

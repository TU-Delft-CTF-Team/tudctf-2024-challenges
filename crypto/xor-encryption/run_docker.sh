#!/bin/sh

docker build -t tudctf/xor-encryption .
docker run -p 5000:5000 --privileged tudctf/xor-encryption
# connect to localhost:5000 to access the challenge

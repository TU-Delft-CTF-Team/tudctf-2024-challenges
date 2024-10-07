#!/bin/sh

docker build -t tudctf/heaps .
docker run -p 5000:5000 --privileged tudctf/heaps
# connect to localhost:5000 to access the challenge
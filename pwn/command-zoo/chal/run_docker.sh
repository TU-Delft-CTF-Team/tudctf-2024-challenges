#!/bin/sh 
docker build -t tudctf/commandzoo . 
docker run -p 5000:5000 --privileged tudctf/commandzoo

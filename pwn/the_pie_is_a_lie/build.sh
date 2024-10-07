#!/bin/sh

docker build --output=. --target=output -f build.Dockerfile .
mv output files
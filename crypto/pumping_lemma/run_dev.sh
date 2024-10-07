#!/bin/sh

cd dist
python3 -m flask -A app:app --debug run
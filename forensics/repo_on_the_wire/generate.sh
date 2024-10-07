#!/usr/bin/env bash

rm -rf repo
mkdir repo
cd repo

flag=$1
blob=$(echo -ne "print('$1')" | base64)
cat > flag.py <<EOF
from base64 import b64decode

exec(b64decode('$blob').decode())
EOF

git init
git branch -m 1337
git config user.name '1337h4xx0r'
git config user.email '1337h4xx0r@haagse-hogeschool.nl'
git add .
git commit -m 'Initial commit'

cat > flag.py <<EOF
print('Hello, World!')
EOF

git add .
git commit -m 'Hello, World!'

touch .git/git-daemon-export-ok

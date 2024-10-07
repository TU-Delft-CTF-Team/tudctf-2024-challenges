FROM pwn.red/jail

COPY --from=ubuntu:22.04@sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658 / /srv

WORKDIR /srv/app

COPY files/chall run
COPY files/flag.txt flag.txt

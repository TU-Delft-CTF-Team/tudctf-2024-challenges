FROM ubuntu:21.04 AS app
FROM pwn.red/jail

COPY --from=app / /srv

WORKDIR /srv/app

COPY files/heaps run
COPY files/flag.txt flag.txt

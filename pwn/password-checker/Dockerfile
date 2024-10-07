FROM ubuntu:22.04 AS app
RUN apt update -y && apt install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY source.c .
RUN gcc -w source.c -fno-stack-protector -o run
RUN pwd
FROM pwn.red/jail
COPY --from=app / /srv

WORKDIR /srv/app

RUN cp /srv/build/run .
COPY flag.txt .

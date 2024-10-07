FROM pwn.red/jail

COPY --from=ubuntu:noble@sha256:8a37d68f4f73ebf3d4efafbcf66379bf3728902a8038616808f04e34a9ab63ee / /srv

WORKDIR /srv/app

COPY files/flowing_over run
COPY files/flag.txt flag.txt

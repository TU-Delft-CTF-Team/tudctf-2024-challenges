FROM python:slim AS app

FROM pwn.red/jail
COPY --from=app / /srv

WORKDIR /srv/app
COPY source.py run
RUN chmod +x run
COPY private.py .
ENV JAIL_MEM=50M JAIL_TIME=60 JAIL_ENV_FLAG=TUDCTF{FAKE_FLAG}

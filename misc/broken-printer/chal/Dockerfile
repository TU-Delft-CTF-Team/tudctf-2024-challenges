FROM pwn.red/jail

COPY --from=python:3.12-slim / /srv
RUN mkdir /srv/app

COPY printer.py /srv/app/run
ENV JAIL_MEM=20M JAIL_ENV_FLAG=TUDCTF{th3re_is_always_an0th3r_w4y}

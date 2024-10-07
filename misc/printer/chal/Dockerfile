FROM pwn.red/jail

COPY --from=python:3.12-slim / /srv
RUN mkdir /srv/app

COPY printer.py /srv/app/run
ENV JAIL_MEM=20M JAIL_ENV_FLAG=TUDCTF{0h_n0_my_print3r_15_h4ck3d}

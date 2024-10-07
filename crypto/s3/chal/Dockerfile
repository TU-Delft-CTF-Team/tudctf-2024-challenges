FROM pwn.red/jail

COPY --from=python:3.12-slim / /srv
RUN mkdir /srv/app

COPY secure-script-service.py /srv/app/run
ENV JAIL_MEM=20M JAIL_ENV_FLAG=TUDCTF{n3ver_d0_y0ur_own_hash1ng_its_4_b4d_id3a}

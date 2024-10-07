FROM pwn.red/jail

COPY --from=python:3.12-slim / /srv
RUN mkdir /srv/app

COPY super-secure-script-service.py /srv/app/run
ENV JAIL_MEM=20M JAIL_ENV_FLAG=TUDCTF{its_st1ll_4_b4d_id3a_what_d1d_you_exp3ct}

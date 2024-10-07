FROM rust:1.81.0-bookworm AS build
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . .
RUN cargo build --release

FROM pwn.red/jail

COPY --from=debian:bookworm-slim / /srv

RUN mkdir /srv/app
COPY --from=build /app/target/release/chronic_flag_capturing_disease /srv/app/run
ENV JAIL_MEM=20M JAIL_TIME=600 JAIL_ENV_FLAG=TUDCTF{FAKE_FLAG}

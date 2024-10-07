FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
	python3 \
	gcc \
	build-essential \
	socat

WORKDIR /app
COPY . /app

RUN chmod +x run.sh

# We use seccomp, so we don't need any of these
RUN gcc -fno-stack-protector -z execstack -no-pie -o architect main.c

EXPOSE 1337 

CMD ./run.sh

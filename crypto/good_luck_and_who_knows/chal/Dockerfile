FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN apt -y update
RUN apt -y install socat

COPY . /app

ENV FLAG=TUDCTF{FAKE_FLAG}

ENTRYPOINT ["./host.sh"]

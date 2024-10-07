FROM python:3.12

RUN apt update -y && apt install -y socat
RUN pip install pycryptodome

WORKDIR /chall

ENV FLAG=TUDCTF{FAKE_FLAG}

COPY source.py .
COPY run.sh .
RUN chmod +x run.sh

CMD ./run.sh
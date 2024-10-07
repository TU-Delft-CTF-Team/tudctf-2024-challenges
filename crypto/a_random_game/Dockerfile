FROM python:3.12

RUN apt update -y && apt install -y socat
RUN pip install pycryptodome

WORKDIR /chall

COPY challenge.py .
COPY run.sh .
RUN chmod +x run.sh

CMD ./run.sh
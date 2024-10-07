FROM python:3.12-alpine

RUN apk add --no-cache socat

WORKDIR /app
COPY jail.py .

CMD ["socat", "TCP-LISTEN:1337,fork", "EXEC:'python3 ./jail.py',stderr,pty,echo=0"]

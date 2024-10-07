FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY app ./app
ENV FLAG=TUDCTF{FAKE_FLAG}

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 5000
CMD ["./entrypoint.sh"]

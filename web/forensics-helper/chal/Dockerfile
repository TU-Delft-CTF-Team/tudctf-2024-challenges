FROM python:3.12-bullseye

WORKDIR /app

RUN apt update && apt install -y exiftool

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app/

ENV FLAG TUDCTF{fake_flag_for_testing}

RUN mkdir /app/uploads

ENV PYTHONUNBUFFERED=1

CMD ["./start.sh"]
EXPOSE 8080

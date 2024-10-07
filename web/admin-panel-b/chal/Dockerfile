FROM python:3.12-bullseye

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app/

ENV FLAG=TUDCTF{fake_flag_for_testing}

RUN python3 init_db.py

RUN useradd -m ctf

USER ctf

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080"]
EXPOSE 8080

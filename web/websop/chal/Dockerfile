FROM python:3.12-alpine


ENV FLAG=TUDCTF{FAKE_FLAG}

COPY webshop/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webshop/ /app
WORKDIR /app

CMD ["python", "-m", "app", "--host", "0.0.0.0", "--port", "8898"]

FROM python:3.12-bookworm


COPY webapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webapp/ /app
WORKDIR /app

ENV FLAG=TUDCTF{FAKE_FLAG}
EXPOSE 8888
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]

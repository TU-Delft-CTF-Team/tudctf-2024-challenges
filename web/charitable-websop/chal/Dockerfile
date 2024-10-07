FROM python:3.12-alpine


ENV FLAG "TUDCTF{g00dw1ll_also_n33ds_s3cur1ty}"

COPY webshop/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webshop/ /app
WORKDIR /app

EXPOSE 8899

CMD ["python", "-m", "app", "--host", "0.0.0.0", "--port", "8899"]

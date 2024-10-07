FROM python:3.12-alpine

ARG FLAG_VALUE="TUDCTF{j4nky_w0nky_th1ng_s3crets_sho0uld_b3_s3cr3ts}"
ENV FLAG $FLAG_VALUE

WORKDIR /app

COPY janky-wonky-thing/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY janky-wonky-thing/ /app

EXPOSE 8000
CMD ["python", "-m", "app", "--host", "0.0.0.0", "--port", "8000"]

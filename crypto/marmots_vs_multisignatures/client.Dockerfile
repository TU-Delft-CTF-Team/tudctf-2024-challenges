FROM python

WORKDIR /chall

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY client.py .

CMD python3 client.py

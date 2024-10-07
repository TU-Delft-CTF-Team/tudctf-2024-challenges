FROM python

WORKDIR /chall

COPY server.py .

EXPOSE 7070
CMD python3 server.py

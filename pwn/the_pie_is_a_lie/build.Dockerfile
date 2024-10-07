FROM ubuntu:22.04@sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658 AS builder

RUN apt update -y && apt install -y gcc build-essential

WORKDIR /output
COPY chall.c .
COPY Makefile .

RUN make chall
RUN echo 'TUDCTF{fake_flag}' > flag.txt

FROM scratch AS output

COPY --from=builder /output/chall /output/chall
COPY --from=builder /output/flag.txt /output/flag.txt
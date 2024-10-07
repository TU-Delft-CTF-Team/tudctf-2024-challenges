# FROM ubuntu:20.04@sha256:85c08a37b74bc18a7b3f8cf89aabdfac51c525cdbc193a753f7907965e310ec2 AS builder

FROM ubuntu:21.04@sha256:ba394fabd516b39ccf8597ec656a9ddd7d0a2688ed8cb373ca7ac9b6fe67848f AS builder
RUN sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
# from now on apt is incredibly slow as it uses old-releases

RUN apt update -y && apt install -y build-essential gcc

WORKDIR /build
COPY heaps.c .
COPY Makefile .
RUN make heaps

RUN mkdir /output && cp /build/heaps /output && cp /lib/x86_64-linux-gnu/libc.so.6 /output && cp /lib64/ld-linux-x86-64.so.2 /output
RUN echo 'TUDCTF{placeholder_flag}' > /output/flag.txt

FROM scratch AS output

WORKDIR output

COPY --from=builder /output .
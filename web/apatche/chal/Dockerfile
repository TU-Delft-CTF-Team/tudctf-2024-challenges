FROM httpd:2.4.49-alpine

COPY ./htdocs/ /usr/local/apache2/htdocs/
COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf

ARG FLAG=TUDCTF{Ap4che_m0r3_l1ke_Unp4tche}
RUN echo "$FLAG" > /flag_$(head -c 4 /dev/urandom | xxd -p).txt

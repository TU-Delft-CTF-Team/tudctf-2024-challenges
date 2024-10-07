FROM gradle:8-jdk21 AS build

COPY backend /app
WORKDIR /app

RUN gradle assemble

FROM eclipse-temurin:21-jre-alpine

ENV FLAG=TUDCTF{FAKE_FLAG}

# Install nginx and supervisor
RUN apk add --update --no-cache nginx supervisor

# Install python3 and pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 py3-pip && ln -sf python3 /usr/bin/python
RUN pip3 install --break-system-packages --no-cache --upgrade pip setuptools

COPY supervisord.conf /etc/supervisord.conf

COPY seed /seed
RUN pip install --break-system-packages -r /seed/requirements.txt

COPY nginx.conf /etc/nginx/http.d/default.conf
COPY --from=build /app/build/libs/XitterBackend-0.0.1-SNAPSHOT.jar /xitter.jar

COPY frontend /frontend

EXPOSE 8880

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

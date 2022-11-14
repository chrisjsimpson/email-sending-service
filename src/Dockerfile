# syntax=docker/dockerfile:1
FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
RUN apk update && apk add incron supervisor
COPY requirements.txt /usr/src/app/
COPY supervisord.conf /etc/supervisord.conf
RUN pip install -r requirements.txt
COPY ./web /usr/src/app/
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

# syntax=docker/dockerfile:1
FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
RUN apk update && apk add incron supervisor curl
COPY requirements.txt /usr/src/app/
COPY supervisord.conf /etc/supervisord.conf
RUN pip install -r requirements.txt
COPY ./web /usr/src/app/
COPY ./entrypoint.sh /

COPY incron.allow /etc/incron.allow

COPY cron-mail /etc/cron.d/cron-mail
RUN crontab /etc/cron.d/cron-mail

RUN adduser -g '' -D mailbox

USER mailbox
RUN mkdir /home/mailbox/letters
COPY push-emails.sh /home/mailbox
RUN echo "/home/mailbox/letters IN_CLOSE_WRITE,loopable=true /bin/sh /home/mailbox/push-emails.sh /home/mailbox/letters" | incrontab -

USER root

ENTRYPOINT ["/entrypoint.sh"]

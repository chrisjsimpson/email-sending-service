#!/bin/sh

touch /home/mailbox/letters/heartbeat
set -euxo

# Adapted from https://github.com/KarmaComputing/send-email-asynchronously/blob/main/push-emails.sh

ME=$(basename "$0");
LCK="/tmp/${ME}.LCK";
exec 8>"$LCK";

flock -x 8;

PATH_TO_EMAILS=$1
echo Running push-emails as "$(whoami)"
# Lossy slow email sender
for EMAIL in $(find "$PATH_TO_EMAILS" -type f)
do
  # listen on host example: nc -k -l 1234
  curl --max-time 2 -v --data-binary @"$EMAIL" host.docker.internal:1234
  rm $EMAIL
done

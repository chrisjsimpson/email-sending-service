#!/bin/sh

set -uxo

# Adapted from https://github.com/KarmaComputing/send-email-asynchronously/blob/main/push-emails.sh

ME=$(basename "$0");
LCK="/tmp/${ME}.LCK";
exec 8>"$LCK";

flock -x 8;

PATH_TO_EMAILS=$1
EMAIL_API_ENDPOINT=$(cat /home/mailbox/EMAIL_API_ENDPOINT)
echo Running push-emails as "$(whoami)"
# Lossy slow email sender
for EMAIL in $(find "$PATH_TO_EMAILS" -type f)
do
  # listen on host example: nc -k -l 1234
  curl --max-time 2 -v --data-binary @"$EMAIL" $EMAIL_API_ENDPOINT
  rm $EMAIL
done

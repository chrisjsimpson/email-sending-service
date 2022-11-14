#!/bin/sh
set -ex

# Because incron does not easily support env
echo -n $EMAIL_API_ENDPOINT > /home/mailbox/EMAIL_API_ENDPOINT

# Start supervisord which start incron & gunicorn
exec /usr/bin/supervisord

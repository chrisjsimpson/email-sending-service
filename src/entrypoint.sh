#!/bin/sh
set -ex

# Start supervisord which start incron & gunicorn
exec /usr/bin/supervisord

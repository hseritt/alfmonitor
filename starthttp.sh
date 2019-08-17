#!/usr/bin/env bash

WSGI_PATH="alfmonitor.wsgi"
LOGDIR="logs"
LOGFILE="$LOGDIR/gunicorn.log"
LOGLEVEL="info"

# If you change this, it must be changed in Apache if you plan to use it
# Apache as a proxy.
PORT=8000
LISTEN=0.0.0.0

gunicorn -b $LISTEN:$PORT --error-logfile $LOGFILE --log-level $LOGLEVEL $WSGI_PATH

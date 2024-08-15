#!/bin/sh
set -e

if [ "$1" = 'gunicorn' ]; then
    shift
    exec gunicorn app.main_api:my_fastapi --config=/docker/gunicorn.conf.py "$@"
fi

exec "$@"

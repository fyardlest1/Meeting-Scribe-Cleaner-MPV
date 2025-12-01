#!/usr/bin/env bash

set -e

# wait for migrations or any other setup tasks
python manage.py migrate --noinput || true


# start Gunicorn server
# gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
exec gunicorn meeting_scribe_mvp.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3

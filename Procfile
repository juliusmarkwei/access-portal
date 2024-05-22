release: python3 manage.py migrate
web: gunicorn core.wsgi:application --log-file -
celeryworker: celery -A core worker & celery -A core beat --loglevel=info & wait -n
celery: celery -A core worker --loglevel=info
celerybeat: celery -A core beat --loglevel=info

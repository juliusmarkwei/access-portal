release: python3 manage.py migrate
web: gunicorn core.wsgi:application --log-file -
worker: celery -A core worker & celery -A core beat --loglevel=info & wait -n
beat: celery -A core beat --loglevel=info
celery: celery -A core worker --loglevel=info

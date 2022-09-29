release: python manage.py migrate --noinput
web: gunicorn ecommerce.wsgi:application --log-file -
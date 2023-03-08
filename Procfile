release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
release: python manage.py collectstatic

web: gunicorn ReceiptGen.wsgi --log-file -
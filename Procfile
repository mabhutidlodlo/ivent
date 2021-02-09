release: python3 manage.py makemigrations --no-input
release: python3 manage.py migrate --no-input

web: daphne -b 0.0.0.0 -p 8001 my_blog.routing:application

worker: python3 manage.py runworker -v2

web: gunicorn my_blog.wsgi

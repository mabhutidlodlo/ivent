release: python3 manage.py makemigrations --no-input
release: python3 manage.py migrate --no-input
web: daphne my_blog.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker -v2




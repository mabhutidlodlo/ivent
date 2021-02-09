release: python3 manage.py makemigrations --no-input
release: python3 manage.py migrate --no-input

web: daphne --ws-protocol "graphql-ws" --proxy-headers my_blog.asgi:channel_layer


worker: python3 manage.py runworker -v2

web: gunicorn my_blog.wsgi

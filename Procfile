release: python3 manage.py makemigrations --no-input
release: python3 manage.py migrate --no-input


web: gunicorn my_blog.wsgi

<<<<<<< HEAD
web: gunicorn Main.wsgi
=======
web: gunicorn Main.wsgi:application --log-file - --log-level debug
heroku ps:scale web=1
python manage.py collectstatic --noinput
>>>>>>> 68366c6132bff41fc1c9c7e7bbf9f2c3413ba670

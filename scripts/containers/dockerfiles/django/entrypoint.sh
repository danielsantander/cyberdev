#!/bin/bash

# Perform any setup tasks here (e.g., migrations, static file collection)

# Abort on any error
# set -e

echo -e "\n---STARTING DJANGO ENTRYPOINT SCRIPT---"

source /.env

echo -e "\n--MAKING MIGRATIONS---"
python3 manage.py makemigrations

echo -e "\n---APPLYING DATABASE MIGRATIONS---"
python3 manage.py migrate

echo -e "\n---MIGRATIONS APPLIED---"
python3 manage.py showmigrations

echo -e "\n---COLLECTING STATIC FILES---"
python3 manage.py collectstatic --noinput

# create superuser, if not exists, using env variables
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    RESULTS=$(python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())")
    SUPERUSER_EXISTS=$(echo $RESULTS | grep -i "False")
    if [ -n "$SUPERUSER_EXISTS" ]; then
        echo -e "\n---SUPERUSER DOES NOT EXIST, CREATING SUPERUSER---"
        python manage.py createsuperuser \
            --noinput \
            --username $DJANGO_SUPERUSER_USERNAME \
            --email $DJANGO_SUPERUSER_EMAIL
    else
        echo -e "\n---SUPERUSER ALREADY EXISTS, SKIPPING CREATION---"
    fi
else
    echo -e "\n---SUPERUSER CREDENTIALS NOT PROVIDED, SKIPPING CREATION---"
fi

echo -e "\n---STARTING GUNICORN SERVER---"
gunicorn --bind 0.0.0.0:8000 app.wsgi:application --reload


#!/bin/sh

echo "Waiting for database..."

python manage.py makemigrations

python manage.py migrate

python manage.py seed_demo

python manage.py runserver 0.0.0.0:8000
#!/bin/sh

echo "Waiting for MySQL Database Service to start..."
# Script from ./wait-for is from:
#...https://github.com/vishnubob/wait-for-it/blob/master/wait-for-it.sh
./wait-for db:3307

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
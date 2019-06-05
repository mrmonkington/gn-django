#!/bin/bash

echo Installing any changed requirements...
.docker/deploy/install_requirements.sh $ENV

cd tests/gn_django_tests
echo Running migrations...
python manage.py migrate

echo Starting Runserver.
exec python manage.py runserver 0.0.0.0:8000
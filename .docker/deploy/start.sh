#!/bin/bash

echo Installing any changed requirements...
.docker/deploy/install_requirements.sh $ENV

echo Waiting for DBs...
.docker/deploy/wait-for-it.sh gravity.mysql:3306 --timeout=30 -- echo "Gravity DB is up."

echo Running gulp...
node_modules/gulp-cli/bin/gulp.js watch &

cd tests/gn_django_tests
echo Running migrations...
python manage.py migrate

echo Starting Runserver.
exec python manage.py runserver 0.0.0.0:8000
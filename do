#!/usr/bin/env bash

if [ $1 = "tests" ]; then
	cd tests
	python manage.py test .
    exit $?
fi

if [ $1 = "coverage" ]; then
    python --version
	coverage erase
	#DJANGO_SETTINGS_MODULE=tests.project.settings \
	#	coverage run `which django-admin` test -v2 tests
	coverage run tests/manage.py test tests/
	coverage report
	coverage html
fi

if [ $1 = "flake8" ]; then
    flake8 gn_django examples tests
fi

if [ $1 = "isort" ]; then
    isort -rc gn_django examples tests
fi

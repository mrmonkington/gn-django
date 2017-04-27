#!/usr/bin/env bash

if [ $1 = "tests" ]; then
	DJANGO_SETTINGS_MODULE=tests.dj_project.settings \
		django-admin test tests
fi

if [ $1 = "coverage" ]; then
    python --version
	coverage erase
	DJANGO_SETTINGS_MODULE=tests.dj_project.settings \
		coverage run `which django-admin` test -v2 tests
	coverage report
	coverage html
fi

if [ $1 = "flake8" ]; then
    flake8 gn_django examples tests
fi

if [ $1 = "isort" ]; then
    isort -rc gn_django examples tests
fi

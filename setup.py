import os
from setuptools import setup, find_packages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
long_description = open(BASE_DIR + '/README.rst').read()

setup(
    name='gn-django',
    version='1.4.0',
    url='https://github.com/gamernetwork/gn-django',
    description='Collection of tools and patterns for Gamer Network django apps/projects.',
    long_description=long_description,
    install_requires=[
        "django==1.11.5",
        "django-jinja==2.3.0",
    ],
    extras_require={
        'selenium': ['selenium==3.3.1'],
        'autocomplete': ['django-autocomplete-light==3.2.9'],
    },
    include_package_data=True,
    author='Brendan Smith',
    author_email='brendan.smith@gamer-network.net',
    scripts = ['gn_django/bin/gn_django', 'gn_django/bin/depstatus'],
    packages = find_packages(exclude=('tests', 'examples')),
)


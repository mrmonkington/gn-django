import os
from setuptools import setup, find_packages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
long_description = open(BASE_DIR + '/README.rst').read()

setup(
    name='gn-django',
    url='https://github.com/gamernetwork/gn-django',
    description='Collection of tools and patterns for Gamer Network django apps/projects.',
    long_description=long_description,
    install_requires=[
        "django>=1.11",
        "django-jinja>=2.2.2",
    ],
    dependency_links = [
    ],
    include_package_data=True,
    scripts = ['gn_django/bin/gn_django'],
    packages = find_packages(),
)

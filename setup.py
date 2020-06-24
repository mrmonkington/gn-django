import os
from setuptools import setup, find_packages

try:
    from gn_django import __version__
except ImportError:
    __version__ = 'dev'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
long_description = open(BASE_DIR + '/README.rst').read()

setup(
    name='gn-django',
    version=__version__,
    url='https://github.com/gamernetwork/gn-django',
    description=("Collection of tools and patterns for Gamer Network django "
            "apps/projects."),
    long_description=long_description,
    install_requires=[
        "django>=2.2,<2.3",
        "django-jinja==2.3.0",
        "pytz",
    ],
    extras_require={
        'selenium': ['selenium==3.3.1', 'splinter==0.8.0'],
        'autocomplete': ['django-autocomplete-light>=3.3,<4.0.0'],
    },
    include_package_data=True,
    author='Gamer Network',
    author_email='tech@gamer-network.net',
    scripts = ['gn_django/bin/gn_django', 'gn_django/bin/depstatus'],
    packages = find_packages(exclude=('tests', 'examples')),
)

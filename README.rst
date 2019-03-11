gn-django
=========

Overview
--------

This library should be the first dependency installed when creating
a Gamer Network django project.  It offers:

* An executable project builder which creates a bootstrapped django project
  following Gamer Network's best practices/patterns.
  ``gn_django startproject myproject``
* An extended jinja templating environment offering context processor 
  functionality and handy filters/globals/extensions.
* A number of extensions for the django ORM for common fields/validation.
* A few helper utility functions and django middlewares for dealing with
  common problems.
* Extensions to django which assist in dealing with a related family of network
  sites, such as 
  `custom jinja loaders <https://gamer-network-gn-django.readthedocs-hosted.com/en/latest/jinja_templates/loaders.html>`_,
  `a site package <https://gamer-network-gn-django.readthedocs-hosted.com/en/latest/packages/site.html#site>`_,
  `a view registry <https://gamer-network-gn-django.readthedocs-hosted.com/en/latest/packages/app.html#view-registry>`_.

gn-django is a library of optional packages; these can be cherry picked 
depending on the needs of the django project that uses it.  However, it is highly 
recommended that the ``gn_django startproject`` builder is used along with the
jinja templating environment provided by gn-django.

Documentation
-------------

gn-django's documentation can be found here: https://gn-docs-propjoe.dev.gamer-network.net/subprojects/gn-django/index.html

Getting Started
---------------

To use gn-django in a django project, just install it with pip in a python3.5 (or greater)
virtualenv:

``pip install gn-django --index-url https://pypi.gamer-network.net/gamernetwork/dev/+simple/``

You may want to follow the instructions on 
`starting a django project <https://gamer-network-gn-django.readthedocs-hosted.com/en/brendan-builder-binary/django_projects/starting_a_project.html>`_.

Tests
-----

To run the tests: 

* Clone the github repository.
* Set up a virtual environment with ``virtualenv -p python3 /path/to/environment``
* Activate the environment with ``source /path/to/environment/bin/activate``
* Run ``tox``

Running the test application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Install docker following the instructions here; https://github.com/gamernetwork/devops/wiki/Using-Docker-for-Platform-Projects
* Run ``cp tests/gn_django_tests/project/settings/local.py.example tests/gn_django_tests/project/settings/local.py`` and adjust any settings if necessary
* Run ``cp .env.example .env`` and adjust if necessary
* Run ``cp docker-compose.override.yml.example docker-compose.override.yml`` and adjust if necessary
* Run ``docker-compose up -d`` to bring up the container and access it in the browser at ``127.0.0.1:11091`` assuming you haven't changed the port number
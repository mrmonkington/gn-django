.. _gn-django-environment-overridable-settings:

Environment-Overridable Settings
================================

Vanilla django projects are setup with a ``settings.py`` file in the 
root of the project.  This isn't fit for purpose when we need to be able to 
override settings for many environments (e.g. dev/beta/staging/production).  Instead, we should have the following file structure:

.. code-block:: bash

    - manage.py
    - project/
        - urls.py
        - wsgi.py
        - settings/
            - __init__.py
            - base.py
            - local.py


.. note:: 

    When working with git, be sure to add ``local.py`` to the ``.gitignore`` 
    file, and duplicate the original as ``example-local.py``, so that it's 
    easy for other developers to set their own custom settings without 
    breaking everyone else's.

In the django project's code, we should still be able to import settings in the 
normal way e.g. ``from django.conf import settings``.  
To do this, we should specify a custom ``__init__.py``. 

.. code-block:: python

    from .local import *

.. note:: 
    
    Our custom ``__init__.py`` is the actual file that's imported when the 
    settings package is imported in python.

Our ``base.py`` should specify sensible defaults and settings that are shared 
between environments, e.g:

.. code-block:: python

    import os
    
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
    
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'p%%wui+wso8!u14#q%5m==*rp(63!zic^3s6z%6$x*qsi-h53-'
    
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    
    ALLOWED_HOSTS = []
    
    
    # Application definition
    
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'articles.apps.ArticlesConfig',
        'taggit',
    ]
    
    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    ROOT_URLCONF = 'admin.urls'
    
    ...
    
    STATIC_URL = '/static/'

``local.py`` should be used to specify environment-specific overrides.

.. code-block:: python

    from .base import *
    
    DATABASES = {
    }
    ...

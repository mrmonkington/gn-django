How to set up Jinja in a django project
=======================================

To use gn-django's jinja template engine, make sure you've installed 
``gn-django`` as a pip dependency.

In your project's ``settings.py``, add the following to the top of the 
``TEMPLATES`` list::

    {
        "BACKEND": "gn_django.template.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            # Try to use jinja when rendering any template, not just one with a
            # particular file extension
            'match_extension': None,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'gn_django.template.context_processors.settings',
            ],
        }
    },


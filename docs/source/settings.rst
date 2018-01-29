.. _gn-django-settings:

Settings
========

Since gn-django is a library of optional components, there are no settings that
are absolutely required by a django project which uses it.  There are settings
related to particular gn-django packages/features, however.

Less Compilation
----------------

If your project makes use of the ``gulpfile.js`` defined in gn-django.

* ``LESS_COMPILATIONS`` - list of dictionaries representing locations of less
  files which need compiling.  This should have keys ``"source"``, ``"destination"`` and ``"watch"``.
  This could be a :ref:`composite setting <gn-django-app-settings>`.

.. _gn-django-settings-staticlink:

Staticlink
----------

- ``STATICLINK_PREPROCESSORS`` - A dictionary mapping script type to preprocessors::

    STATICLINK_PREPROCESSORS = {
      'css': 'less',
    }
- ``STATICLINK_CLIENT_COMPILERS`` - A dictionary mapping script type to the URLs of client-side compilation scripts::

    STATICLINK_CLIENT_COMPILERS = {
        'css': '//cdnjs.cloudflare.com/ajax/libs/less.js/2.7.1/less.min.js',
    }

- ``STATICLINK_DEBUG`` - This option allows you to enable or disable debug mode for different script types::

    STATICLINK_DEBUG = {
       'css': False,
       'js': True,
    }

- ``STATICLINK_FILE_MAP`` - A dictionary mapping file extensions to directory. If it is not set, it will default to a directory of the same name as the file extension::

    STATICLINK_FILE_MAP = {
       'js': 'scripts',
       'less': 'precompiled',
    }

- ``STATICLINK_VERSION`` - A unique version number to append to the static file URLs for cache-busting. Defaults to current time stamp.

.. _gn-django-app-settings:

``app_settings.py`` and Composite Settings
------------------------------------------

Gamer Network has a number of django apps which are designed to be used
together in concrete django projects.  It's handy for these apps to be able to provide their
own settings - which can be overridden by project settings.  To achieve this,
we will follow a convention of creating a module ``app_settings.py`` in our 
django applications.

``app_settings.py`` should be used to provide sensible defaults for app-specific
settings, but it could also be used to provide values for what we will call
"composite settings".  A composite setting is a setting whose concrete value
should be assembled by combining composite values from different apps' 
``app_settings.py`` modules.  For example, say that we have many locations 
of less files to compile - across a number of django apps - each app should define
a ``LESS_COMPILATIONS`` setting which is assembled in the django project's 
settings file.

Settings contained in ``app_settings.py`` must be used in a final settings file
explicitly, there is no automatic mechanism for including them in the settings
namespace.

Environment Overridable Settings
--------------------------------

Be sure to also read up on :ref:`environment overridable settings <gn-django-environment-overridable-settings>`.

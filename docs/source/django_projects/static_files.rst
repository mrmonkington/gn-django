Developing with Static Files
============================

Usage in Templates
------------------

GN Django comes with a Jinja extension for linking to static files using the ``css``
and ``js`` tags. For more information on usage and configuration, see the
:ref:`documentation <gn-django-static-link>`.

Compilation
-----------

GN Django is agnostic to what is used for static file compilation. However,
it is recommended to use `Gulp <http://gulpjs.com/>`_, and the binary installer
automatically generates ``packages.json`` and ``gulpfile.js`` to handle
installation, file watching and asset generation.

Gulp Installation
~~~~~~~~~~~~~~~~~

To use Gulp, you'll then need to install the dependencies defined in the ``packages.json`` file
by running::

  npm install

from the main project root. This will install the dependencies into the ``node_modules``
directory.

Gulp Compilation Tasks
~~~~~~~~~~~~~~~~~~~~~~

To watch your static files and compile automatically, run::

  node_modules/gulp-cli/bin/gulp.js watch --silent &

This will print the process number for the watcher and then leave it running silently in the background.
The behaviour of the tasks is defined in the ``gulpfile.js`` file.

To use the gulpfile properly, the ``LESS_COMPILATIONS`` setting should be defined. See :ref:`gn-django-settings`.

Here's the standard ``gulpfile.js`` which we use: https://github.com/gamernetwork/gn-django/blob/develop/gn_django/bin/startproject/gulpfile.js

Two commands are defined,
``compile`` and ``watch``. The ``compile`` task does the hard work of compiling
the stylesheets, while the ``watch`` task watches the static LESS files for changes
and compiles accordingly.

Within the ``compile`` command, the following happens:

- ``python manage.py get_less_compilations`` is called to get a JSON iterable of compilation locations.
  For more detail, refer to: :ref:`gn-django-commands-less-compilations`.
- For each compilation location..
  - ``gulp.src()`` command collects files within the ``./static/less`` directory, excluding those in the ``modules`` and ``helpers`` subdirectory.
  - It is then piped to the ``less()`` command, which compiles them into CSS
  - The compiled CSS is then minified by the ``minify()`` command
  - Browser prefixes (such as ``-webkit-``) are automatically added by the ``autoprefixer`` command
  - The compiled CSS files are saved to ``./static/css`` with names matching those of the original files
- You have an uncle named Bob

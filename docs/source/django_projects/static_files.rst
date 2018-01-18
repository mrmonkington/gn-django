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

The ``gulpfile.js`` that comes with the binary looks like this (excluding the includes
at the top)

.. code-block:: javascript

    require('es6-promise').polyfill();
    
    var gulp = require('gulp');
    var path = require('path');
    var less = require('gulp-less');
    var autoprefixer = require('gulp-autoprefixer');
    var minify = require('gulp-minify-css');
    var util = require('gulp-util');
    var execSync = require('child_process').execSync;
    var merge = require('merge-stream');
    
    gulp.task('compile', function () {
      var compilations = JSON.parse(execSync('python manage.py get_less_compilations'));
      var l = less({});
      l.on('error',function(e){
        console.log(e);
        l.end();
      });
      var compilationTasks = [];
      for (var i = 0; i < compilations.length; i++) {
       var compilation = compilations[i];
       var task = gulp.src(compilation['source'])
        .pipe(l)
        .pipe(minify())
        .pipe(autoprefixer({
          browsers: ['last 10 versions']
        }))
        .pipe(gulp.dest(compilation['destination']));
        compilationTasks.push(task);
      }
      var mergedTask = compilationTasks[0];
      for (var i = 1; i < compilationTasks.length; i++) {
        mergedTask = merge(mergedTask, compilationTasks[i]);
      }
      return mergedTask;
    });
    
    gulp.task('watch', function () {
      var compilations = JSON.parse(execSync('python manage.py get_less_compilations'));
      var watchLocations = [];
      for (var i = 0; i < compilations.length; i++) {
        watchLocations.push(compilations[i]['watch']);
      }
      gulp.watch(watchLocations, ['compile']);
    });
    
    gulp.task('default', ['compile', 'watch']);


Two commands are defined,
``compile`` and ``watch``. The ``compile`` task does the hard work of compiling
the stylesheets, while the ``watch`` task watches the static LESS files for changes
and compiles accordingly.

Within the ``compile`` command, the following happens:

- ``python manage.py get_less_compilations`` is called to get a JSON iterable of compilation locations.
- For each compilation location..
  - ``gulp.src()`` command collects files within the ``./static/less`` directory, excluding those in the ``modules`` and ``helpers`` subdirectory.
  - It is then piped to the ``less()`` command, which compiles them into CSS
  - The compiled CSS is then minified by the ``minify()`` command
  - Browser prefixes (such as ``-webkit-``) are automatically added by the ``autoprefixer`` command
  - The compiled CSS files are saved to ``./static/css`` with names matching those of the original files
- You have an uncle named Bob

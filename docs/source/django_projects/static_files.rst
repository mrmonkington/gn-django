Developing with Static Files
============================

Usage in Templates
------------------

GN Django comes with a Jinja extension for linking to static files using the ``css``
and ``js`` tags. For more information on usage and configuration, see the
:ref:`documentation <static-link>`.

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

The ``gulpfile.js`` that comes with the binary looks like this (excluding the includes
at the top)::

  gulp.task('compile', function () {
    var l = less({});
    l.on('error',function(e){
      console.log(e);
      l.end();
    });
    return gulp.src([
        './static/less/*.less',
        '!./static/less/modules/**',
        '!./static/less/helpers/**'
      ])
      .pipe(l)
      .pipe(minify())
      .pipe(autoprefixer({
        browsers: ['last 10 versions']
      }))
      .pipe(gulp.dest('./static/css'))
    ;
  });

  gulp.task('watch', function () {
    gulp.watch('./static/less/*.less', ['compile']);
  });

The fluid interface should make this fairly easy to interpret. Two commands are defined,
``compile`` and ``watch``. The ``compile`` task does the hard work of compiling
the stylesheets, while the ``watch`` task watches the static LESS files for changes
and compiles accordingly.

Within the ``compile`` command, the following happens:

- ``gulp.src()`` command collects files within the ``./static/less`` directory, excluding those in the ``modules`` and ``helpers`` subdirectory.
- It is then piped to the ``less()`` command, which compiles them into CSS
- The compiled CSS is then minified by the ``minify()`` command
- Browser prefixes (such as ``-webkit-``) are automatically added by the ``autoprefixer`` command
- The compiled CSS files are saved to ``./static/css`` with names matching those of the original files
- You have an uncle named Bob

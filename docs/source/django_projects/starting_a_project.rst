Starting a django project
=========================

There is a builder binary included as part of ``gn-django`` which makes
creating a Gamer Network django project easy.  

To use it, follow these steps: 
  *  `create a >=python3.5 virtualenv <https://github.com/gamernetwork/devops/wiki/Python-Tips#virtualenv>`_ and activate it.
  * Run ``pip install git+ssh://git@github.com/gamernetwork/gn-django.git`` to install ``gn-django`` in to the virtualenv.
  * Now you can run ``gn_django startproject <projectname> [<path_to_project>]``.

This will create a django project called ``<projectname>`` in the current directory
(or specified directory, if you use the second optional argument).

The project is set up with the following:

  * A standard ``manage.py`` for running the project.
  * A ``project/`` directory containing:

      * :ref:`environment-overridable-settings`
      * A ``wsgi.py`` file
      * A root ``urls.py`` file
  * A ``.gitignore`` file which ignores a sensible default of files.
  * A ``.github`` file which defines a basic Pull Request template for github repos.
  * A basic ``requirements.txt`` file which includes ``gn-django`` as a requirement.

The default project settings include ``django-jinja`` as an installed app
and set up a jinja template backend as :ref:`explained here <how-to-set-up-jinja>` 
which matches jinja templates (ending with `".j2"`) in all apps' `templates/` 
directories.

The project should be runnable immediately with all setup boilerplate taken
care of.

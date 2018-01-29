.. _gn-django-commands:

Commands
========

``gn_django.commands`` is a very lightweight django app which provides a number
of helper commands.

.. _gn-django-commands-less-compilations:

``get_less_compilations``
-------------------------

The ``get_less_compilations`` command prints a JSON string of the ``LESS_COMPILATIONS``
setting for the django project.

``LESS_COMPILATIONS`` should be a python list comprised of dictionaries, like so:

.. code:: python
    
    LESS_COMPILATIONS = [
        {
            "source": os.path.join(app_path, 'static/less/cms/*.less'),
            "destination": os.path.join(app_path, 'static/css/cms/'),
            "watch": os.path.join(app_path, 'static/less/cms/**/*.less'),
        }
    ]

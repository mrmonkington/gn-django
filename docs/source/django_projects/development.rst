Developing a django project
===========================

Django debug toolbar
--------------------

Django debug toolbar is very handy when developing django projects.  It gives
a simple profile of the request, DB query information, template rendering info,
settings, headers etc etc.

Particularly useful is the DB query information which can greatly assist in
optimising the use of the django ORM.

Installing
^^^^^^^^^^

It's simple to install django debug toolbar, follow these steps:

  * Follow the instructions detailed `here <https://django-debug-toolbar.readthedocs.io/en/stable/installation.html>`_
  * Ensure that the extra settings to add the toolbar are only in your ``local.py``
  * Add the following to the ``local.py``:
    
    .. code-block:: python

        def show_toolbar(request):
            """
            Default function to determine whether to show the toolbar on a given page.
            """
            return bool(DEBUG)
        
        DEBUG_TOOLBAR_CONFIG = {
            "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
        }

Logging
-------

TODO

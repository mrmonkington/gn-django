.. _package-db:

DB
==

The ``db`` package contains functionality relating to dealing with the
django database layer.

The ``gn_django.db.db_routers.AppsRouter`` class
------------------------------------------------

A router to route DB operations for one or more django apps to a particular 
database.

Subclasses of ``AppsRouter`` can specify django app labels and a database name
to route DB operations to.

Requires subclasses to specify class attributes:
  * `APPS` - an iterable of django app labels
  * `DB_NAME` - a string for the DB to route operations to

e.g.

.. code-block:: python

    from gn_django.db.db_routers import AppsRouter

    class AuthRouter(AppsRouter):
        
        APPS = ['auth', 'barristan']
        DB_NAME = 'auth_db'

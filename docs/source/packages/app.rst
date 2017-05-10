.. _package-app:

App
===

.. _app-configs:

App configs
-----------

The ``app`` package defines a custom ``AppConfig`` class called ``GNAppConfig``
which should be used by django apps which depend on gn-django features.  It's
a drop-in replacement for django's standard ``AppConfig`` class in django's built
in `applications library <https://docs.djangoproject.com/en/1.11/ref/applications/>`_.
Right now, the only extended functionality that it offers is to allow django
apps to register views for combining in to a :ref:`view-registry`.  In future,
it may offer additional functionality for app-specific configuration.

.. _view-registry:

View Registry
-------------

The view registry allows django apps to progressively override the class based
view that will service a particular url.

Using the registry means we do not need to duplicate url patterns in multiple
apps' ``urls.py`` files.  Views in ``urls.py`` are referenced by a registry 
lookup using a label as opposed to a concrete reference to a view class.

An app registers View classes to the registry by declaring a 
:ref:`GNAppConfig <app_configs>` subclass in ``apps.py``.  This class should
have a class attribute ``views`` which is a dictionary composed of view labels 
and view classes.

All apps' app configs are iterated over to build the global view registry for
a django project.  This occurs the first time that a view is queried for using
the ``gn_django.app.view_registry.get()`` function.
The project view registry is populated in the order of ``settings.INSTALLED_APPS``
so that subsequent apps can override the views of preceding apps - this means
that apps lower in ``INSTALLED_APPS`` will override apps that are higher.

Example
~~~~~~~

To illustrate, it's best to work through an example.  Say that we have a 
``content`` app followed by a ``eurogamer`` app in 
``settings.INSTALLED_APPS``.  The ``content`` app registers a view in 
``content/apps.py`` as follows:

.. code-block:: python

    from gn_django.app import GNAppConfig

    from . import views

    class ContentApp(GNAppConfig):
        name = 'content'
        view_registry = {
            'content:ArticleView': views.ArticleView,
        }

This is referenced in ``content/urls.py`` file, like so:

.. code-block:: python

    from django.conf.urls import url
    from django.contrib import admin
    
    from gn_django.app import view_registry
    
    urlpatterns = [
        url(r'^article$', view_registry.get('content:ArticleView')),
    ]

The ``eurogamer`` app is able to override that view in it's 
``eurogamer/apps.py`` like so:

.. code-block:: python

    from gn_django.app import GNAppConfig

    from . import views

    class EurogamerApp(GNAppConfig):
        name = 'eurogamer'
        view_registry = {
            'content:ArticleView': views.EurogamerArticleView,
        }

This means that when the url is resolved for a request to ``/article``, it 
resolves to the ``eurogamer`` app's ``views.EurogamerArticleView`` for processing.

Reference
---------

.. automodule:: gn_django.app.view_registry
   :members:

.. automodule:: gn_django.app.app_config
   :members:

.. _package-view:

View
====

View Registry
-------------

The view registry allows django apps to progressively override the class based
view that will service a particular url.

Using the registry means we do not need to duplicate url patterns in multiple
apps' ``urls.py`` files.  Views in ``urls.py`` are referenced by a registry 
lookup using a label as opposed to a concrete reference to a view class.

An app registers ``View`` classes to the registry in a ``registered_views.py`` file.
All apps' ``registered_views.py`` files are included when the django application 
is started.
The view registry is populated in the order of ``settings.INSTALLED_APPS`` 
so that subsequent apps can override the views of preceding apps - this means
that apps that are lower in ``INSTALLED_APPS`` will override views for apps that 
are higher.

Example
~~~~~~~

To illustrate, it's best to work through an example.  Say that we have a 
``content`` app followed by a ``eurogamer`` app in 
``settings.INSTALLED_APPS``.  The ``content`` app registers a view in 
``content/registered_views.py`` as follows:

.. code-block:: python

   from gn_django.view import view_registry

   from . import views

   view_registry.register("content:ArticleView", views.ArticleView)

This is referenced in ``content/urls.py`` file, like so:

.. code-block:: python

    from django.conf.urls import url
    from django.contrib import admin
    
    from gn_django.view import view_registry
    
    urlpatterns = [
        url(r'^article$', view_registry.get('content:ArticleView')),
    ]

The ``eurogamer`` app is able to override that view in it's 
``eurogamer/registered_views.py`` like so:

.. code-block:: python

   from gn_django.view import view_registry

   from . import views as eurogamer_views

   view_registry.register("content:ArticleView", eurogamer_views.EurogamerArticleView)

This means that when the url is resolved for a request to ``/article``, it 
resolves to the ``eurogamer`` app's ``views.EurogamerArticleView`` for processing.

Reference
---------

.. automodule:: gn_django.view.view_registry
   :members:

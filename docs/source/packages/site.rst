Site 
====

The ``site`` package contains functionality to make a django project
globally aware of the site that is being processed in the current 
request.

Using the site package 
----------------------

The site package is most useful when a particular django project/deployment
can service multiple different sites.  e.g. traffic for 
"www.metabomb.net" and "www.eurogamer.net" goes to the same django deployment.

There is a middleware ``gn_django.site.middleware.SiteFromDomainMiddleware``
which can be added to django's ``MIDDLEWARE`` setting.  This will 
identify the current site by interrogating the Host header sent in a 
request e.g. a Host ``www.eurogamer.net`` is for the site ``eurogamer.net``.  
The middleware sets the site value using ``gn_django.site.set_current_site``
- which in turn saves the site value in thread local storage.  This means
that any application code within the request-response cycle can use
``gn_django.site.get_current_site`` to act conditionally on the current
site.  

There's a few things that should be considered when writing code that uses
``gn_django.site.get_current_site``:
  * The approach is pretty much a copy of django's built in i18n framework;
    where a language can be activated and the current language can be 
    interrogated.
  * It's best to limit code that depends on ``get_current_site`` to be in the
    view layer as much as possible.  model-layer code is able to import and
    interrogate the current site, but thought should be put in to whether the
    current site will be set by all callers - e.g. management tasks, external
    services which share model code, etc.
  * Middleware ordering matters, middleware run before the 
    ``SiteFromDomainMiddleware`` class will not be able to use site features.

It's possible that in future, we could alternatively identify the
current site by inspecting the requested URL e.g. ``auth.gamer-network.net/eurogamer/...``

Steps
~~~~~

To use the site package for domain-based site identification, follow these steps:
  * Add ``gn_django.site.middleware.SiteFromDomainMiddleware`` to 
    the django ``MIDDLEWARE`` setting.
  * Add a ``SITE_DOMAINS`` dictionary to your django settings - this should map
    request Host values to site strings. e.g. 
    ``SITE_DOMAINS = {'www.eurogamer.net': 'eurogamer.net'}``
  * **OPTIONAL** Add a ``SITE_NAMESPACES`` dictionary to your django settings - 
    this should map site values to a namespace string. e.g. 
    ``SITE_NAMESPACES = {'eurogamer.net': 'eurogamer_net'}``

A word on thread local storage
------------------------------

The ``site`` package makes use of thread local storage in order to persist the 
current site for the duration of a request.  This is essentially a safe way to
make some state global to a django application.

A kneejerk response to this might be 'globals are bad!' which is a healthy
consideration to have.  In this case, the assumption is that most application
code will need to have a common way of figuring out what the current site is and
that this shared hook is vastly more preferable to bloating interfaces with too
many extra ``site`` parameters.

Generally, the use of TLS needs to be considered on a case by case basis.

Reference
---------

.. automodule:: gn_django.site
   :members:

.. automodule:: gn_django.site.middleware
   :members:

.. automodule:: gn_django.site.middleware
   :members:

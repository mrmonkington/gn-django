Custom Loaders
==============

Loaders are responsible for loading templates from a resource such as the file 
system.  See `the jinja documentation for more detail <http://jinja.pocoo.org/docs/2.9/api/#loaders>`_.  
The most common loader in use is the ``FileSystemLoader`` which loads templates
from files on the local filesystem - it's instantiated with a searchpath for
a directory of templates.

This type of Loader is great for a single site or application which has a 
well defined focus, however if we have complex template requirements we can use a custom loader.
There's an easy mechanism to specify custom loaders for a jinja backend which
allows developers to specify the ``Loader`` object to use in django settings.

Sparse template inheritance
---------------------------

Sparse template inheritance is the idea that a given template identifier can 
resolve to many different concrete template files depending on the makeup of 
a template **hierarchy**.  The inheritance chain for templates
is dependent on the active **hierarchy** rather than being static.  So, if we 
have a django app that can be used for many different sites, sparse template
inheritance affords us the ability to override the templates that are used
at runtime depending on the active template **hierarchy**.  Say we have a generalised
``"article.html"`` template in our common templates directory - this can be overridden 
easily for a given site by inserting a template directory in to the hierarchy 
which defines it.  View code can remain unchanged.

The idea came about to solve the problem of major duplication between templates
for a related family of sites.  Broadly, most content sites can share a lot of 
core structure since they are all solving the fundamental problem of surfacing
content to users.  In Gamer Network, we have a few different site **hierarchies**
which can be represented as a tree::

                                                       +-----------------+
                                                       |                 |
                           +---------------------------+  gamer network  +------------------------------+
                           |                       |   |                 |    |                         |
                           |                       |   +-----------------+    |                         |
                           |                       |                          |                         |
                           |                       |                          |                         |
                           |                       |                          |                         |
                           |                       |                          |                         |
                 +-------------------+    +-------------------+     +-------------------+    +-------------------+
                 |                   |    |                   |     |                   |    |                   |
            +----+       vg247       |    |     eurogamer     |     |      usgamer      |    |    jelly deals    |
            |    |                   |    |                   |     |                   |    |                   |
            |    +-------------------+    +---------------------+   +-------------------+    +-------------------+
            |               |                  |                |
            |               |                  |                |
            |               |                  |                |
      +-----------+  +-----------+      +--------------+  +--------------+
      |           |  |           |      |              |  |              |
      | vg247.com |  | vg247.pl  |      | eurogamer.net|  | eurogamer.pl |
      |           |  |           |      |              |  |              |
      +-----------+  +-----------+      +--------------+  +--------------+
    

The tree represents the logical groupings and ancestry of site properties
at Gamer Network.  It makes sense for our template code to be able to make use of
this ancestry.  Hopefully the majority of template code will be in common for 
all of Gamer Network content sites, and only certain parts of templates
will need overrides at different levels of the **hierarchy**.

**For any given site, the template hierarchy - inheritance chain that should be taken
through the tree - is defined and is static.**

The idea of a **template hierarchy** for a given site is key: the **hierarchy**
is the path that is taken through the tree to get to a concrete site.
In practical terms, this means that nodes in the tree end up as directories of
templates and they are linked together by the **hierarchy** which acts as a 
chain of inheritance.

Let's transpose this tree in to a template **hierarchy** for `eurogamer.net`.  We have a template directory
for each node of our tree.  Say that the root node is called `core` - that node
contains base defaults for page templates, widgets, etc. On the next level, 
`eurogamer` contains templates (which may inherit from core) which have overrides
for eurogamer-family specifc structure.  And then `eurogamer_net` contains 
templates which inherit and override others in the **hierarchy** for template 
code that is truly site specific.

The great thing about sparse template inheritance is that it can be done 
without any special view code - so an ``ArticleView`` just renders a template
identified as ``article.j2``.  The view doesn't care that the **hierarchy**
used grabbed the template from the ``eurogamer`` directory instead of the ``core`` 
directory.  

The **hierarchy** to follow for loading the 
template for a particular site is defined up front and given to a
custom ``Loader`` class which is able to traverse the hierarchy and load
the correct template.

Sparse template inheritance in practice
---------------------------------------

To use sparse template inheritance in a django project, you must use either the
:ref:`gn-django-hierarchy-loader` or :ref:`gn-django-multi-hierarchy-loader` classes.  

The :ref:`gn-django-hierarchy-loader` is for use when your deployable django project is
for one concrete site - i.e. there is a single template inheritance hierarchy 
to resolve.  In this case, we may have a ``eurogamer`` repository which has django
apps for ``eurogamer_net``, ``eurogamer_de``, ``eurogamer_pl`` etc.  Each of 
these different apps would have their own template directories and overridden 
backend code - so there would need to be a separate deployment per site.  In this
case we can use the :ref:`gn-django-hierarchy-loader` because a given django deployment has
a single static hierarchy to resolve.

The :ref:`gn-django-multi-hierarchy-loader` is for use when your deployable django project is
for multiple concrete sites - i.e. there are many inheritance hierarchies that
the loader will need to resolve. For example, the auth service will have a 
web app frontend for setting user profiles/changing passwords etc. Each 
instance of the auth frontend will need to be able to serve any of the 
following domains: auth.eurogamer.net, auth.eurogamer.de, auth.usgamer.net, etc. 
The core auth functionality between different sites is unlikely to differ 
beyond needing feature toggles, but we do need to be able to have site-specific 
frontends and override the templates used in a nice way.  So the 
:ref:`gn-django-multi-hierarchy-loader` is used for selecting the appropriate template 
hierarchy to use for each request.

Using the HierarchyLoader
~~~~~~~~~~~~~~~~~~~~~~~~~

**Note**: This worked example is runnable in ``examples/sparse_inheritance/``.

The instantiated :ref:`gn-django-hierarchy-loader` should be passed to the jinja backend
in the ``TEMPLATES`` django setting.

.. code-block:: python

    from gn_django.template.loaders import get_hierarchy_loader
    TEMPLATE_BASE = os.path.join(BASE_DIR, 'templates')
    # Define your template hierarchy here - most specific to least specific
    loader = get_hierarchy_loader([
        ('eurogamer_net', os.path.join(TEMPLATE_BASE, 'eurogamer_net')),
        ('eurogamer', os.path.join(TEMPLATE_BASE, 'eurogamer')),
        ('core', os.path.join(TEMPLATE_BASE, 'core')),
    ])
    
    TEMPLATES = [
        {
            "BACKEND": "gn_django.template.backend.Jinja2",
            "APP_DIRS": True,
            "OPTIONS": {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'gn_django.template.context_processors.settings',
                ],
                'loader': loader,
            }
        },
    ]

.. note::
    :ref:`get_hierarchy_loader <gn-django-get-hierarchy-loader>` is a simple convenience method which allows us to
    specify the template hierarchy as a simple list of namespace identifier/template directory 
    pairs.  Under the hood, it instantiates a loader hierarchy composed
    of ``FileSystemLoaders`` for each namespace/directory pair which allows templates
    to be loaded by ancestry, by namespace or by sequential lookup.

.. _gn-django-hierarchy-template-loading:

Now, when rendering templates from a view, the :ref:`gn-django-hierarchy-loader` will be 
used.  It's used for any template loading within jinja; loading the
template to render for a view as well as for ``extends``, ``include``, ``macro``
etc template tags within templates.

The loader offers three formats of template lookup:

  * **ancestor lookup** - ``<loader>_parent:base.j2`` - this will attempt to find
    the closest ancestor template that matches below the named loader
    in the loader hierarchy.
  
  * **namespace lookup** - ``<loader>:base.j2`` - this will attempt to find the `base.j2`
    template from the specified named loader in the loader hierarchy.
  
  * **sequential lookup** - ``base.j2`` - this will attempt to find the `base.j2`
    template by trying all of the loaders in the loader hierarchy, sequentially.

**Examples:**

.. code-block:: python

    hierarchy_loader.get_source(env, 'eurogamer_parent:base.j2')

Will yield `base.j2` from the `'core'` loader and will
otherwise raise a `DjangoTemplateNotFoundException` if it cannot find it.

.. code-block:: python

    hierarchy_loader.get_source(env, 'core:foo.j2')

Will yield `foo.j2` from the `'core'` loader if it exists and will
otherwise raise a `DjangoTemplateNotFoundException` if it cannot find it.

.. code-block:: python

    hierarchy_loader.get_source(env, 'bar.j2')

Will find `bar.j2` by querying the loaders sequentially from ``eurogamer_net``
to ``core``.


Using the MultiHierarchyLoader in conjunction with the site package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** This worked example is runnable in ``examples/sparse_inheritance_multi_site/``.

As mentioned, the :ref:`gn-django-multi-hierarchy-loader` is for use when your deployable 
django project will service multiple concrete sites.
This might be achieved by domain separation - e.g. ``"auth.eurogamer.net"`` and 
``"auth.vg247.com"``.  Or it might be achieved by URL path separation - e.g. 
``"auth.gamer-network.net/eurogamer_net/"`` and ``auth.gamer-network.net/vg247_com/``. 
Right now, only domain separation has been implemented with use of 
:ref:`the site package<gn-django-package-site>`.

The instantiated :ref:`gn-django-multi-hierarchy-loader` should be passed to the jinja backend
in the ``TEMPLATES`` django setting.

.. code-block:: python

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # SiteFromDomainMiddleware is needed to make the domain for each
        # request globally available
        'gn_django.site.middleware.SiteFromDomainMiddleware',
    ]

    from gn_django.template.loaders import get_multi_hierarchy_loader
    TEMPLATE_BASE = os.path.join(BASE_DIR, 'templates')
    # Define all of the loader hierarchies for all sites
    loader = get_multi_hierarchy_loader(
        # callback function for loader to use to work out the current site
        # and thus which HierarchyLoader to use
        "gn_django.site.get_namespace_for_site",
        # Each hierarchy has a namespace identifier and a directory hierarchy
        (
            ('eurogamer_net', (
                ('eurogamer_net', os.path.join(TEMPLATE_BASE, 'eurogamer_net')),
                ('eurogamer', os.path.join(TEMPLATE_BASE, 'eurogamer')),
                ('core', os.path.join(TEMPLATE_BASE, 'core')),
            )),
            ('eurogamer_de', (
                ('eurogamer_de', os.path.join(TEMPLATE_BASE, 'eurogamer_de')),
                ('eurogamer', os.path.join(TEMPLATE_BASE, 'eurogamer')),
                ('core', os.path.join(TEMPLATE_BASE, 'core')),
            )),
            ('vg247_com', (
                ('vg247_com', os.path.join(TEMPLATE_BASE, 'vg247_com')),
                ('vg247', os.path.join(TEMPLATE_BASE, 'vg247')),
                ('core', os.path.join(TEMPLATE_BASE, 'core')),
            )),
            ('vg247_pl', (
                ('vg247_pl', os.path.join(TEMPLATE_BASE, 'vg247_pl')),
                ('vg247', os.path.join(TEMPLATE_BASE, 'vg247')),
                ('core', os.path.join(TEMPLATE_BASE, 'core')),
            )),
        )
    )
    
    # Mapping of Host domain values to site identifiers
    SITE_DOMAINS = {
        "127.0.0.1": "eurogamer.net",
        "eurogamer.net.local": "eurogamer.net",
        "eurogamer.de.local": "eurogamer.de",
        "vg247.com.local": "vg247.com",
        "vg247.pl.local": "vg247.pl",
    }
    
    # Mapping of site identifiers to namespace identifiers
    SITE_NAMESPACES = {
        "eurogamer.net": "eurogamer_net",
        "eurogamer.de": "eurogamer_de",
        "vg247.com": "vg247_com",
        "vg247.pl": "vg247_pl",
    }
    
    TEMPLATES = [
        {
            "BACKEND": "gn_django.template.backend.Jinja2",
            "APP_DIRS": True,
            "OPTIONS": {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'gn_django.template.context_processors.settings',
                ],
                'loader': loader,
                'template_cache_key_cb': 'gn_django.site.template.get_template_cache_key_with_site',
            }
        },
    ]

.. note::
    :ref:`get_multi_hierarchy_loader <gn-django-get-multi-hierarchy-loader>` is a convenience method which allows us to
    specify the template hierarchies as a nested data structure.  Under the hood, 
    it instantiates a :ref:`gn-django-hierarchy-loader` for each template hierarchy 
    specified.  It also takes a callback function to use by the loader to
    resolve which hierarchy is active at any given time - so that the correct
    :ref:`gn-django-hierarchy-loader` is used to load templates.

Template loading is delegated to the :ref:`gn-django-hierarchy-loader` and follows the
:ref:`conventions defined previously<gn-django-hierarchy-template-loading>`.  The 
difference is that the :ref:`gn-django-hierarchy-loader` used to load templates is selected
based on the result of the ``gn_django.site.get_namespace_for_site`` callback 
function.  So the loader is chosen based on the domain of the current request -
set by the :ref:`SiteFromDomainMiddleware <gn-django-site-from-domain-middleware>`.

Reference
---------

.. _gn-django-hierarchy-loader:

HierarchyLoader
~~~~~~~~~~~~~~~

.. autoclass:: gn_django.template.loaders.HierarchyLoader
   :members:


.. _gn-django-multi-hierarchy-loader:

MultiHierarchyLoader
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: gn_django.template.loaders.MultiHierarchyLoader
   :members:

Helpers
~~~~~~~

.. _gn-django-get-hierarchy-loader:

.. autofunction:: gn_django.template.loaders.get_hierarchy_loader

.. _gn-django-get-multi-hierarchy-loader:

.. autofunction:: gn_django.template.loaders.get_multi_hierarchy_loader


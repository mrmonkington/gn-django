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
the template **hierarchy** and that the inheritance chain for those templates
is dependent on an active **hierarchy** rather than being static.  

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
templates which inherit and override others in the **hierarchy** for structure that
is truly site specific.

For any given site, the template **hierarchy** - inheritance chain that should be taken
through the tree - is defined and is static.
The great thing about sparse template inheritance is that it can be done 
without any special view code - so an ``ArticleView`` just renders a template
identified as ``article.html``.  The view doesn't care that the **hierarchy**
used grabbed the template from the ``eurogamer`` directory instead of the ``core`` 
directory.  

The **hierarchy** to follow for loading the 
template for a particular site is defined up front and given to a
custom ``Loader`` class which is able to traverse the hierarchy and load
the correct template.

Sparse template inheritance in practice
---------------------------------------

To use sparse template inheritance in a django project, you must use either the
:ref:`hierarchy-loader` or :ref:`multi-hierarchy-loader` classes.  

The :ref:`hierarchy-loader` is for use when your deployable django project is
for one concrete site - i.e. there is a single template inheritance hierarchy 
to resolve.

The :ref:`multi-hierarchy-loader` is for use when your deployable django project is
for multiple concrete sites - i.e. there are many inheritance hierarchies that
the loader will need to resolve.

Using the HierarchyLoader
~~~~~~~~~~~~~~~~~~~~~~~~~

**Note**: This worked example is runnable in ``examples/sparse_inheritance/``.

The instantiated :ref:`hierarchy-loader` should be passed to the jinja backend
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
                'match_extension': None,
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
    :ref:`get_hierarchy_loader <get-hierarchy-loader>` is a simple convenience method which allows us to
    specify the template hierarchy as a simple list of namespace identifier/template directory 
    pairs.  Under the hood, it instantiates a loader hierarchy composed
    of ``FileSystemLoaders`` for each namespace/directory pair which allows templates
    to be loaded by ancestry, by namespace or by sequential lookup.

.. _hierarchy-template-loading:

Now, when rendering templates from a view, the :ref:`hierarchy-loader` will be 
used.  It's used for any template loading within jinja; loading the
template to render for a view as well as for ``extends``, ``include``, ``macro``
etc template tags within templates.

The loader offers three formats of template lookup:

  * **ancestor lookup** - ``<loader>_parent:base.html`` - this will attempt to find
    the closest ancestor template that matches below the named loader
    in the loader hierarchy.
  
  * **namespace lookup** - ``<loader>:base.html`` - this will attempt to find the `base.html`
    template from the specified named loader in the loader hierarchy.
  
  * **sequential lookup** - ``base.html`` - this will attempt to find the `base.html`
    template by trying all of the loaders in the loader hierarchy, sequentially.
    Note: If the other two methods fail, sequential lookup is the fallback.

**Examples:**

.. code-block:: python

    hierarchy_loader.get_source(env, 'eurogamer_parent:base.html')

Will yield `base.html` from the `'core'` loader and will
otherwise try to find it sequentially from eurogamer to core:

.. code-block:: python

    hierarchy_loader.get_source(env, 'core:foo.html')

Will yield `foo.html` from the `'core'` loader if it exists and will
otherwise try to find it sequentially from the ``eurogamer`` loader to ``core``:

.. code-block:: python

    hierarchy_loader.get_source(env, 'bar.html')

Will find `bar.html` by querying the loaders sequentially from ``eurogamer_net``
to ``core``.


Using the MultiHierarchyLoader in conjunction with the site package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** This worked example is runnable in ``examples/sparse_inheritance_multi_site/``.

As mentioned, the :ref:`multi-hierarchy-loader` is for use when your deployable 
django project will service multiple concrete sites.
This might be achieved by domain separation - e.g. ``"auth.eurogamer.net"`` and 
``"auth.vg247.com"``.  Or it might be achieved by URL path separation - e.g. 
``"auth.gamer-network.net/eurogamer_net/"`` and ``auth.gamer-network.net/vg247_com/``. 
Right now, only domain separation has been implemented with use of 
:ref:`the site package<package-site>`.

The instantiated :ref:`multi-hierarchy-loader` should be passed to the jinja backend
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
                'match_extension': None,
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
    :ref:`get_multi_hierarchy_loader <get-multi-hierarchy-loader>` is a convenience method which allows us to
    specify the template hierarchies as a nested data structure.  Under the hood, 
    it instantiates a :ref:`hierarchy-loader` for each template hierarchy 
    specified.  It also takes a callback function to use by the loader to
    resolve which hierarchy is active at any given time - so that the correct
    :ref:`hierarchy-loader` is used to load templates.

Template loading is delegated to the :ref:`hierarchy-loader` and follows the
:ref:`conventions defined previously<hierarchy-template-loading>`.  The 
difference is that the :ref:`hierarchy-loader` used to load templates is selected
based on the result of the ``gn_django.site.get_namespace_for_site`` callback 
function.  So the loader is chosen based on the domain of the current request -
set by the :ref:`SiteFromDomainMiddleware <site-from-domain-middleware>`.

Reference
---------

.. _hierarchy-loader:

HierarchyLoader
~~~~~~~~~~~~~~~

.. autoclass:: gn_django.template.loaders.HierarchyLoader
   :members:


.. _multi-hierarchy-loader:

MultiHierarchyLoader
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: gn_django.template.loaders.MultiHierarchyLoader
   :members:

Helpers
~~~~~~~

.. _get-hierarchy-loader:

.. autofunction:: gn_django.template.loaders.get_hierarchy_loader

.. _get-multi-hierarchy-loader:

.. autofunction:: gn_django.template.loaders.get_multi_hierarchy_loader


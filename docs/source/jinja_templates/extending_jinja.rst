Extending Jinja templates
=========================

Context processors
------------------

There is a mechanism to ensure that all templates rendered by django views
include some context which is global to your application.

The ``context_processors`` option is a list of callables – called context 
processors – that take a request object as their argument and return a 
dictionary of items to be merged into the context.

Context processors are applied on top of context data. This means that a 
context processor may overwrite variables you’ve supplied to your view
context, so take care to avoid variable names that overlap with those 
supplied by your context processors.

To use context processors, specify them in the jinja backend of your
``TEMPLATES`` setting::

    "OPTIONS": {
        "context_processors": [
            "navigation.context_processors.global_nav",
        ],
    }


Registering per-application globals and filters
-----------------------------------------------

django-jinja comes with facilities for loading template filters, globals 
and tests from django applications.

Here's an example::

    # <someapp>/templatetags/<anyfile>.py
    # don't forget to create __init__.py in templatetags dir
    
    from django_jinja import library
    import jinja2
    
    @library.test(name="one")
    def is_one(n):
        """
        Usage: {% if m is one %}Foo{% endif %}
        """
        return n == 1
    
    @library.filter
    def mylower(name):
        """
        Usage: {{ 'Hello'|mylower() }}
        """
        return name.lower()
    
    @library.filter
    @jinja2.contextfilter
    def replace(context, value, x, y):
        """
        Filter with template context. Usage: {{ 'Hello'|replace('H','M') }}
        """
        return value.replace(x, y)
    
    
    @library.global_function
    def myecho(data):
        """
        Usage: {{ myecho('foo') }}
        """
        return data
    
    
    @library.global_function
    @library.render_with("test-render-with.jinja")
    def myrenderwith(*args, **kwargs):
        """
        Render result with jinja template. Usage: {{ myrenderwith() }}
        """
        return {"name": "Foo"}
    
    
    from .myextensions  import MyExtension
    library.extension(MyExtension)


Extending globals, filters and tests provided by gn-django
----------------------------------------------------------

In addition to registering globals, filters and tests for specific django 
projects/applications it's possible to extend the defaults provided by the
gn-django library.

This can be achieved by extending the ``Jinja2`` class in ``gn_django.template.backend``.
``get_base_extensions()``, ``get_base_filters()``, ``get_base_tests()`` and
``get_base_globals()`` can all be extended to supplement the default make up
of gn_django's template environment.  
There is no default list of context processors, since adding global context
for the template rendering environment should be done intentionally due to the
possible collisions with context variables provided by views.

**Note:** Any additions made here will be introduced to all Gamer Network django
projects - so they should be generic enough for that to make sense.

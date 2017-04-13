.. templatetag:: static

``static``
~~~~~~~~~~

To link to static files that are saved in :setting:`STATIC_ROOT` Django ships
with a :ttag:`static` template tag. If the :mod:`django.contrib.staticfiles`
app is installed, the tag will serve files using ``url()`` method of the
storage specified by :setting:`STATICFILES_STORAGE`. For example::

    {% load static %}
    <img src="{% static "images/hi.jpg" %}" alt="Hi!" />

It is also able to consume standard context variables, e.g. assuming a
``user_stylesheet`` variable is passed to the template::

    {% load static %}
    <link rel="stylesheet" href="{% static user_stylesheet %}" type="text/css" media="screen" />

If you'd like to retrieve a static URL without displaying it, you can use a
slightly different call::

    {% load static %}
    {% static "images/hi.jpg" as myphoto %}
    <img src="{{ myphoto }}"></img>

.. admonition:: Using Jinja2 templates?

    See :class:`~django.template.backends.jinja2.Jinja2` for information on
    using the ``static`` tag with Jinja2.


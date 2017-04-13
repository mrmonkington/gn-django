.. templatetag:: url

.. function:: url

    Returns an absolute path reference (a URL without the domain name) matching a
    given view and optional parameters. Any special characters in the resulting
    path will be encoded using :func:`~django.utils.encoding.iri_to_uri`.
    
    This is a way to output links without violating the DRY principle by having to
    hard-code URLs in your templates::
    
        {% url 'some-url-name' v1 v2 %}
    
    The first argument is a :func:`~django.conf.urls.url` ``name``. It can be a
    quoted literal or any other context variable. Additional arguments are optional
    and should be space-separated values that will be used as arguments in the URL.
    The example above shows passing positional arguments. Alternatively you may
    use keyword syntax::
    
        {% url 'some-url-name' arg1=v1 arg2=v2 %}
    
    Do not mix both positional and keyword syntax in a single call. All arguments
    required by the URLconf should be present.
    
    For example, suppose you have a view, ``app_views.client``, whose URLconf
    takes a client ID (here, ``client()`` is a method inside the views file
    ``app_views.py``). The URLconf line might look like this:
    
    .. code-block:: python
    
        ('^client/([0-9]+)/$', app_views.client, name='app-views-client')
    
    If this app's URLconf is included into the project's URLconf under a path
    such as this:
    
    .. code-block:: python
    
        ('^clients/', include('project_name.app_name.urls'))
    
    ...then, in a template, you can create a link to this view like this::
    
        {% url 'app-views-client' client.id %}
    
    The template tag will output the string ``/clients/client/123/``.
    
    Note that if the URL you're reversing doesn't exist, you'll get an
    :exc:`~django.urls.NoReverseMatch` exception raised, which will cause your
    site to display an error page.
    
    If you'd like to retrieve a URL without displaying it, you can use a slightly
    different call::
    
        {% url 'some-url-name' arg arg2 as the_url %}
    
        <a href="{{ the_url }}">I'm linking to {{ the_url }}</a>
    
    The scope of the variable created by the  ``as var`` syntax is the
    ``{% block %}`` in which the ``{% url %}`` tag appears.
    
    This ``{% url ... as var %}`` syntax will *not* cause an error if the view is
    missing. In practice you'll use this to link to views that are optional::
    
        {% url 'some-url-name' as the_url %}
        {% if the_url %}
          <a href="{{ the_url }}">Link to optional stuff</a>
        {% endif %}
    
    If you'd like to retrieve a namespaced URL, specify the fully qualified name::
    
        {% url 'myapp:view-name' %}
    
    This will follow the normal :ref:`namespaced URL resolution strategy
    <topics-http-reversing-url-namespaces>`, including using any hints provided
    by the context as to the current application.
    
    .. warning::
    
        Don't forget to put quotes around the :func:`~django.conf.urls.url`
        ``name``, otherwise the value will be interpreted as a context variable!
    
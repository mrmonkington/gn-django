.. templatetag:: get_media_prefix

.. function:: get_media_prefix

    Similar to the :ttag:`get_static_prefix`, ``get_media_prefix`` populates a
    template variable with the media prefix :setting:`MEDIA_URL`, e.g.::
    
        {% load static %}
        <body data-media-url="{% get_media_prefix %}">
    
    By storing the value in a data attribute, we ensure it's escaped appropriately
    if we want to use it in a JavaScript context.
    
    ===========================
    ``django.contrib.humanize``
    ===========================
    
    .. module:: django.contrib.humanize
       :synopsis: A set of Django template filters useful for adding a "human
                  touch" to data.
    
    A set of Django template filters useful for adding a "human touch" to data.
    
    To activate these filters, add ``'django.contrib.humanize'`` to your
    :setting:`INSTALLED_APPS` setting. Once you've done that, use
    ``{% load humanize %}`` in a template, and you'll have access to the following
    filters.
    
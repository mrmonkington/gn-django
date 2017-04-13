.. templatetag:: get_static_prefix

.. function:: get_static_prefix

    You should prefer the :ttag:`static` template tag, but if you need more control
    over exactly where and how :setting:`STATIC_URL` is injected into the template,
    you can use the :ttag:`get_static_prefix` template tag::
    
        {% load static %}
        <img src="{% get_static_prefix %}images/hi.jpg" alt="Hi!" />
    
    There's also a second form you can use to avoid extra processing if you need
    the value multiple times::
    
        {% load static %}
        {% get_static_prefix as STATIC_PREFIX %}
    
        <img src="{{ STATIC_PREFIX }}images/hi.jpg" alt="Hi!" />
        <img src="{{ STATIC_PREFIX }}images/hi2.jpg" alt="Hello!" />
    
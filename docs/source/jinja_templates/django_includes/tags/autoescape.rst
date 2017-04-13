.. templatetag:: autoescape

.. function:: autoescape

    Controls the current auto-escaping behavior. This tag takes either ``on`` or
    ``off`` as an argument and that determines whether auto-escaping is in effect
    inside the block. The block is closed with an ``endautoescape`` ending tag.
    
    When auto-escaping is in effect, all variable content has HTML escaping applied
    to it before placing the result into the output (but after any filters have
    been applied). This is equivalent to manually applying the :tfilter:`escape`
    filter to each variable.
    
    The only exceptions are variables that are already marked as "safe" from
    escaping, either by the code that populated the variable, or because it has had
    the :tfilter:`safe` or :tfilter:`escape` filters applied.
    
    Sample usage::
    
        {% autoescape on %}
            {{ body }}
        {% endautoescape %}
    
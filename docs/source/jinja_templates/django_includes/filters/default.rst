.. templatefilter:: default

.. function:: default

    If value evaluates to ``False``, uses the given default. Otherwise, uses the
    value.
    
    For example::
    
        {{ value|default:"nothing" }}
    
    If ``value`` is ``""`` (the empty string), the output will be ``nothing``.
    
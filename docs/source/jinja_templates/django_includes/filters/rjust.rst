.. templatefilter:: rjust

.. function:: rjust

    Right-aligns the value in a field of a given width.
    
    **Argument:** field size
    
    For example::
    
        "{{ value|rjust:"10" }}"
    
    If ``value`` is ``Django``, the output will be ``"    Django"``.
    
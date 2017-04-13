.. templatefilter:: last

.. function:: last

    Returns the last item in a list.
    
    For example::
    
        {{ value|last }}
    
    If ``value`` is the list ``['a', 'b', 'c', 'd']``, the output will be the
    string ``"d"``.
    
.. templatefilter:: slice

.. function:: slice

    Returns a slice of the list.
    
    Uses the same syntax as Python's list slicing. See
    http://www.diveintopython3.net/native-datatypes.html#slicinglists
    for an introduction.
    
    Example::
    
        {{ some_list|slice:":2" }}
    
    If ``some_list`` is ``['a', 'b', 'c']``, the output will be ``['a', 'b']``.
    
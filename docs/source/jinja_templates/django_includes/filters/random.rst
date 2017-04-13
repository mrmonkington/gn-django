.. templatefilter:: random

.. function:: random

    Returns a random item from the given list.
    
    For example::
    
        {{ value|random }}
    
    If ``value`` is the list ``['a', 'b', 'c', 'd']``, the output could be ``"b"``.
    
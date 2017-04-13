.. templatefilter:: linenumbers

.. function:: linenumbers

    Displays text with line numbers.
    
    For example::
    
        {{ value|linenumbers }}
    
    If ``value`` is::
    
        one
        two
        three
    
    the output will be::
    
        1. one
        2. two
        3. three
    
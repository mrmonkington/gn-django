.. templatefilter:: truncatewords

.. function:: truncatewords

    Truncates a string after a certain number of words.
    
    **Argument:** Number of words to truncate after
    
    For example::
    
        {{ value|truncatewords(2) }}
    
    If ``value`` is ``"Joel is a slug"``, the output will be ``"Joel is ..."``.
    
    Newlines within the string will be removed.
    
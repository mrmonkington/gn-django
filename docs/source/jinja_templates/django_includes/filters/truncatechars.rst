.. templatefilter:: truncatechars

.. function:: truncatechars

    Truncates a string if it is longer than the specified number of characters.
    Truncated strings will end with a translatable ellipsis sequence ("...").
    
    **Argument:** Number of characters to truncate to
    
    For example::
    
        {{ value|truncatechars(9) }}
    
    If ``value`` is ``"Joel is a slug"``, the output will be ``"Joel i..."``.
    
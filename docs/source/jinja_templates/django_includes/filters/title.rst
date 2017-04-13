.. templatefilter:: title

.. function:: title

    Converts a string into titlecase by making words start with an uppercase
    character and the remaining characters lowercase. This tag makes no effort to
    keep "trivial words" in lowercase.
    
    For example::
    
        {{ value|title }}
    
    If ``value`` is ``"my FIRST post"``, the output will be ``"My First Post"``.
    
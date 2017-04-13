.. templatefilter:: slugify

.. function:: slugify

    Converts to ASCII. Converts spaces to hyphens. Removes characters that aren't
    alphanumerics, underscores, or hyphens. Converts to lowercase. Also strips
    leading and trailing whitespace.
    
    For example::
    
        {{ value|slugify }}
    
    If ``value`` is ``"Joel is a slug"``, the output will be ``"joel-is-a-slug"``.
    
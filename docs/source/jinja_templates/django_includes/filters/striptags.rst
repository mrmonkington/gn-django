.. templatefilter:: striptags

.. function:: striptags

    Makes all possible efforts to strip all [X]HTML tags.
    
    For example::
    
        {{ value|striptags }}
    
    If ``value`` is ``"<b>Joel</b> <button>is</button> a <span>slug</span>"``, the
    output will be ``"Joel is a slug"``.
    
    .. admonition:: No safety guarantee
    
        Note that ``striptags`` doesn't give any guarantee about its output being
        HTML safe, particularly with non valid HTML input. So **NEVER** apply the
        ``safe`` filter to a ``striptags`` output. If you are looking for something
        more robust, you can use the ``bleach`` Python library, notably its
        `clean`_ method.
    
    .. _clean: https://bleach.readthedocs.io/en/latest/clean.html
    
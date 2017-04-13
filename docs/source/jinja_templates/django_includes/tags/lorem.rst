.. templatetag:: lorem

.. function:: lorem

    Displays random "lorem ipsum" Latin text. This is useful for providing sample
    data in templates.
    
    Usage::
    
        {% lorem [count] [method] [random] %}
    
    The ``{% lorem %}`` tag can be used with zero, one, two or three arguments.
    The arguments are:
    
    ===========  =============================================================
    Argument     Description
    ===========  =============================================================
    ``count``    A number (or variable) containing the number of paragraphs or
                 words to generate (default is 1).
    ``method``   Either ``w`` for words, ``p`` for HTML paragraphs or ``b``
                 for plain-text paragraph blocks (default is ``b``).
    ``random``   The word ``random``, which if given, does not use the common
                 paragraph ("Lorem ipsum dolor sit amet...") when generating
                 text.
    ===========  =============================================================
    
    Examples:
    
    * ``{% lorem %}`` will output the common "lorem ipsum" paragraph.
    * ``{% lorem 3 p %}`` will output the common "lorem ipsum" paragraph
      and two random paragraphs each wrapped in HTML ``<p>`` tags.
    * ``{% lorem 2 w random %}`` will output two random Latin words.
    
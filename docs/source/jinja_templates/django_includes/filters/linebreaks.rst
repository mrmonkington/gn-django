.. templatefilter:: linebreaks

.. function:: linebreaks

    Replaces line breaks in plain text with appropriate HTML; a single
    newline becomes an HTML line break (``<br />``) and a new line
    followed by a blank line becomes a paragraph break (``</p>``).
    
    For example::
    
        {{ value|linebreaks }}
    
    If ``value`` is ``Joel\nis a slug``, the output will be ``<p>Joel<br />is a
    slug</p>``.
    
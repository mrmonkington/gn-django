.. templatefilter:: force_escape

.. function:: force_escape

    Applies HTML escaping to a string (see the :tfilter:`escape` filter for
    details). This filter is applied *immediately* and returns a new, escaped
    string. This is useful in the rare cases where you need multiple escaping or
    want to apply other filters to the escaped results. Normally, you want to use
    the :tfilter:`escape` filter.
    
    For example, if you want to catch the ``<p>`` HTML elements created by
    the :tfilter:`linebreaks` filter::
    
        {% autoescape off %}
            {{ body|linebreaks|force_escape }}
        {% endautoescape %}
    
.. templatefilter:: escape

.. function:: escape

    Escapes a string's HTML. Specifically, it makes these replacements:
    
    * ``<`` is converted to ``&lt;``
    * ``>`` is converted to ``&gt;``
    * ``'`` (single quote) is converted to ``&#39;``
    * ``"`` (double quote) is converted to ``&quot;``
    * ``&`` is converted to ``&amp;``
    
    Applying ``escape`` to a variable that would normally have auto-escaping
    applied to the result will only result in one round of escaping being done. So
    it is safe to use this function even in auto-escaping environments. If you want
    multiple escaping passes to be applied, use the :tfilter:`force_escape` filter.
    
    For example, you can apply ``escape`` to fields when :ttag:`autoescape` is off::
    
        {% autoescape off %}
            {{ title|escape }}
        {% endautoescape %}
    
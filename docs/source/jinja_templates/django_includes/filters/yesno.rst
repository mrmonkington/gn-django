.. templatefilter:: yesno

.. function:: yesno

    Maps values for ``True``, ``False``, and (optionally) ``None``, to the strings
    "yes", "no", "maybe", or a custom mapping passed as a comma-separated list, and
    returns one of those strings according to the value:
    
    For example::
    
        {{ value|yesno("yeah,no,maybe") }}
    
    ==========  ======================  ===========================================
    Value       Argument                Outputs
    ==========  ======================  ===========================================
    ``True``                            ``yes``
    ``True``    ``"yeah,no,maybe"``     ``yeah``
    ``False``   ``"yeah,no,maybe"``     ``no``
    ``None``    ``"yeah,no,maybe"``     ``maybe``
    ``None``    ``"yeah,no"``           ``no`` (converts ``None`` to ``False``
                                        if no mapping for ``None`` is given)
    ==========  ======================  ===========================================
    
    
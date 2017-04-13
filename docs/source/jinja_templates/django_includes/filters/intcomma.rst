.. templatefilter:: intcomma

.. function:: intcomma

    Converts an integer or float (or a string representation of either) to a string
    containing commas every three digits.
    
    Examples:
    
    * ``4500`` becomes ``4,500``.
    * ``4500.2`` becomes ``4,500.2``.
    * ``45000`` becomes ``45,000``.
    * ``450000`` becomes ``450,000``.
    * ``4500000`` becomes ``4,500,000``.
    
    :doc:`/topics/i18n/formatting` will be respected if enabled,
    e.g. with the ``'de'`` language:
    
    * ``45000`` becomes ``'45.000'``.
    * ``450000`` becomes ``'450.000'``.
    
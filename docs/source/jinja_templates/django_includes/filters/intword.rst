.. templatefilter:: intword

.. function:: intword

    Converts a large integer (or a string representation of an integer) to a
    friendly text representation. Works best for numbers over 1 million.
    
    Examples:
    
    * ``1000000`` becomes ``1.0 million``.
    * ``1200000`` becomes ``1.2 million``.
    * ``1200000000`` becomes ``1.2 billion``.
    
    Values up to 10^100 (Googol) are supported.
    
    :doc:`/topics/i18n/formatting` will be respected if enabled,
    e.g. with the ``'de'`` language:
    
    * ``1000000`` becomes ``'1,0 Million'``.
    * ``1200000`` becomes ``'1,2 Million'``.
    * ``1200000000`` becomes ``'1,2 Milliarden'``.
    
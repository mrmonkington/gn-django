.. templatefilter:: time

.. function:: time

    Formats a time according to the given format.
    
    Given format can be the predefined one :setting:`TIME_FORMAT`, or a custom
    format, same as the :tfilter:`date` filter. Note that the predefined format
    is locale-dependent.
    
    For example::
    
        {{ value|time("H:i") }}
    
    If ``value`` is equivalent to ``datetime.datetime.now()``, the output will be
    the string ``"01:23"``.
    
    Another example:
    
    Assuming that :setting:`USE_L10N` is ``True`` and :setting:`LANGUAGE_CODE` is,
    for example, ``"de"``, then for::
    
        {{ value|time("TIME_FORMAT") }}
    
    the output will be the string ``"01:23"`` (The ``"TIME_FORMAT"`` format
    specifier for the ``de`` locale as shipped with Django is ``"H:i"``).
    
    The ``time`` filter will only accept parameters in the format string that
    relate to the time of day, not the date (for obvious reasons). If you need to
    format a ``date`` value, use the :tfilter:`date` filter instead (or along
    ``time`` if you need to render a full :py:class:`~datetime.datetime` value).
    
    There is one exception the above rule: When passed a ``datetime`` value with
    attached timezone information (a :ref:`time-zone-aware
    <naive_vs_aware_datetimes>` ``datetime`` instance) the ``time`` filter will
    accept the timezone-related :ref:`format specifiers
    <date-and-time-formatting-specifiers>` ``'e'``, ``'O'`` , ``'T'`` and ``'Z'``.
    
    When used without a format string, the ``TIME_FORMAT`` format specifier is
    used::
    
        {{ value|time }}
    
    is the same as::
    
        {{ value|time("TIME_FORMAT") }}
    
    .. versionchanged:: 1.10
    
        In older versions, the :setting:`TIME_FORMAT` setting (without
        localization) is always used when a format string isn't given.
    
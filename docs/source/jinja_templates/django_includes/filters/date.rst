.. templatefilter:: date

.. function:: date

    Formats a date according to the given format.
    
    Uses a similar format as PHP's ``date()`` function (https://php.net/date)
    with some differences.
    
    .. note::
        These format characters are not used in Django outside of templates. They
        were designed to be compatible with PHP to ease transitioning for designers.
    
    .. _date-and-time-formatting-specifiers:
    
    Available format strings:
    
    ================  ========================================  =====================
    Format character  Description                               Example output
    ================  ========================================  =====================
    a                 ``'a.m.'`` or ``'p.m.'`` (Note that       ``'a.m.'``
                      this is slightly different than PHP's
                      output, because this includes periods
                      to match Associated Press style.)
    A                 ``'AM'`` or ``'PM'``.                     ``'AM'``
    b                 Month, textual, 3 letters, lowercase.     ``'jan'``
    B                 Not implemented.
    c                 ISO 8601 format. (Note: unlike others     ``2008-01-02T10:30:00.000123+02:00``,
                      formatters, such as "Z", "O" or "r",      or ``2008-01-02T10:30:00.000123`` if the datetime is naive
                      the "c" formatter will not add timezone
                      offset if value is a naive datetime
                      (see :class:`datetime.tzinfo`).
    d                 Day of the month, 2 digits with           ``'01'`` to ``'31'``
                      leading zeros.
    D                 Day of the week, textual, 3 letters.      ``'Fri'``
    e                 Timezone name. Could be in any format,
                      or might return an empty string,          ``''``, ``'GMT'``, ``'-500'``, ``'US/Eastern'``, etc.
                      depending on the datetime.
    E                 Month, locale specific alternative
                      representation usually used for long
                      date representation.                      ``'listopada'`` (for Polish locale, as opposed to ``'Listopad'``)
    f                 Time, in 12-hour hours and minutes,       ``'1'``, ``'1:30'``
                      with minutes left off if they're zero.
                      Proprietary extension.
    F                 Month, textual, long.                     ``'January'``
    g                 Hour, 12-hour format without leading      ``'1'`` to ``'12'``
                      zeros.
    G                 Hour, 24-hour format without leading      ``'0'`` to ``'23'``
                      zeros.
    h                 Hour, 12-hour format.                     ``'01'`` to ``'12'``
    H                 Hour, 24-hour format.                     ``'00'`` to ``'23'``
    i                 Minutes.                                  ``'00'`` to ``'59'``
    I                 Daylight Savings Time, whether it's       ``'1'`` or ``'0'``
                      in effect or not.
    j                 Day of the month without leading          ``'1'`` to ``'31'``
                      zeros.
    l                 Day of the week, textual, long.           ``'Friday'``
    L                 Boolean for whether it's a leap year.     ``True`` or ``False``
    m                 Month, 2 digits with leading zeros.       ``'01'`` to ``'12'``
    M                 Month, textual, 3 letters.                ``'Jan'``
    n                 Month without leading zeros.              ``'1'`` to ``'12'``
    N                 Month abbreviation in Associated Press    ``'Jan.'``, ``'Feb.'``, ``'March'``, ``'May'``
                      style. Proprietary extension.
    o                 ISO-8601 week-numbering year,             ``'1999'``
                      corresponding to the ISO-8601 week
                      number (W) which uses leap weeks. See Y
                      for the more common year format.
    O                 Difference to Greenwich time in hours.    ``'+0200'``
    P                 Time, in 12-hour hours, minutes and       ``'1 a.m.'``, ``'1:30 p.m.'``, ``'midnight'``, ``'noon'``, ``'12:30 p.m.'``
                      'a.m.'/'p.m.', with minutes left off
                      if they're zero and the special-case
                      strings 'midnight' and 'noon' if
                      appropriate. Proprietary extension.
    r                 :rfc:`5322` formatted date.               ``'Thu, 21 Dec 2000 16:01:07 +0200'``
    s                 Seconds, 2 digits with leading zeros.     ``'00'`` to ``'59'``
    S                 English ordinal suffix for day of the     ``'st'``, ``'nd'``, ``'rd'`` or ``'th'``
                      month, 2 characters.
    t                 Number of days in the given month.        ``28`` to ``31``
    T                 Time zone of this machine.                ``'EST'``, ``'MDT'``
    u                 Microseconds.                             ``000000`` to ``999999``
    U                 Seconds since the Unix Epoch
                      (January 1 1970 00:00:00 UTC).
    w                 Day of the week, digits without           ``'0'`` (Sunday) to ``'6'`` (Saturday)
                      leading zeros.
    W                 ISO-8601 week number of year, with        ``1``, ``53``
                      weeks starting on Monday.
    y                 Year, 2 digits.                           ``'99'``
    Y                 Year, 4 digits.                           ``'1999'``
    z                 Day of the year.                          ``0`` to ``365``
    Z                 Time zone offset in seconds. The          ``-43200`` to ``43200``
                      offset for timezones west of UTC is
                      always negative, and for those east of
                      UTC is always positive.
    ================  ========================================  =====================
    
    For example::
    
        {{ value|date("D d M Y") }}
    
    If ``value`` is a :py:class:`~datetime.datetime` object (e.g., the result of
    ``datetime.datetime.now()``), the output will be the string
    ``'Wed 09 Jan 2008'``.
    
    The format passed can be one of the predefined ones :setting:`DATE_FORMAT`,
    :setting:`DATETIME_FORMAT`, :setting:`SHORT_DATE_FORMAT` or
    :setting:`SHORT_DATETIME_FORMAT`, or a custom format that uses the format
    specifiers shown in the table above. Note that predefined formats may vary
    depending on the current locale.
    
    Assuming that :setting:`USE_L10N` is ``True`` and :setting:`LANGUAGE_CODE` is,
    for example, ``"es"``, then for::
    
        {{ value|date("SHORT_DATE_FORMAT") }}
    
    the output would be the string ``"09/01/2008"`` (the ``"SHORT_DATE_FORMAT"``
    format specifier for the ``es`` locale as shipped with Django is ``"d/m/Y"``).
    
    When used without a format string, the ``DATE_FORMAT`` format specifier is
    used. Assuming the same settings as the previous example::
    
        {{ value|date }}
    
    outputs ``9 de Enero de 2008`` (the ``DATE_FORMAT`` format specifier for the
    ``es`` locale is ``r'j \d\e F \d\e Y'``.
    
    .. versionchanged:: 1.10
    
        In older versions, the :setting:`DATE_FORMAT` setting (without
        localization) is always used when a format string isn't given.
    
    You can combine ``date`` with the :tfilter:`time` filter to render a full
    representation of a ``datetime`` value. E.g.::
    
        {{ value|date("D d M Y") }} {{ value|time("H:i") }}
    
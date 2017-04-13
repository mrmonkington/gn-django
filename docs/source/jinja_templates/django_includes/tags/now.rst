.. templatetag:: now

``now``
-------

Displays the current date and/or time, using a format according to the given
string. Such string can contain format specifiers characters as described
in the :tfilter:`date` filter section.

Example::

    It is {% now "jS F Y H:i" %}

Note that you can backslash-escape a format string if you want to use the
"raw" value. In this example, both "o" and "f" are backslash-escaped, because
otherwise each is a format string that displays the year and the time,
respectively::

    It is the {% now "jS \o\f F" %}

This would display as "It is the 4th of September".

.. note::

    The format passed can also be one of the predefined ones
    :setting:`DATE_FORMAT`, :setting:`DATETIME_FORMAT`,
    :setting:`SHORT_DATE_FORMAT` or :setting:`SHORT_DATETIME_FORMAT`.
    The predefined formats may vary depending on the current locale and
    if :doc:`/topics/i18n/formatting` is enabled, e.g.::

        It is {% now "SHORT_DATETIME_FORMAT" %}

You can also use the syntax ``{% now "Y" as current_year %}`` to store the
output (as a string) inside a variable. This is useful if you want to use
``{% now %}`` inside a template tag like :ttag:`blocktrans` for example::

    {% now "Y" as current_year %}
    {% blocktrans %}Copyright {{ current_year }}{% endblocktrans %}


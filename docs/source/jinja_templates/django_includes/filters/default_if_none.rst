.. templatefilter:: default_if_none

``default_if_none``
-------------------

If (and only if) value is ``None``, uses the given default. Otherwise, uses the
value.

Note that if an empty string is given, the default value will *not* be used.
Use the :tfilter:`default` filter if you want to fallback for empty strings.

For example::

    {{ value|default_if_none:"nothing" }}

If ``value`` is ``None``, the output will be ``nothing``.


.. templatefilter:: length_is

``length_is``
-------------

Returns ``True`` if the value's length is the argument, or ``False`` otherwise.

For example::

    {{ value|length_is:"4" }}

If ``value`` is ``['a', 'b', 'c', 'd']`` or ``"abcd"``, the output will be
``True``.


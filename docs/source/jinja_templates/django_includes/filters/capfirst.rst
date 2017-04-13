.. templatefilter:: capfirst

``capfirst``
------------

Capitalizes the first character of the value. If the first character is not
a letter, this filter has no effect.

For example::

    {{ value|capfirst }}

If ``value`` is ``"django"``, the output will be ``"Django"``.


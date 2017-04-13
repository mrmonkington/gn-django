.. templatefilter:: cut

``cut``
-------

Removes all values of arg from the given string.

For example::

    {{ value|cut:" " }}

If ``value`` is ``"String with spaces"``, the output will be
``"Stringwithspaces"``.


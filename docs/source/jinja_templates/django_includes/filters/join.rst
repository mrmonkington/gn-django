.. templatefilter:: join

``join``
--------

Joins a list with a string, like Python's ``str.join(list)``

For example::

    {{ value|join:" // " }}

If ``value`` is the list ``['a', 'b', 'c']``, the output will be the string
``"a // b // c"``.


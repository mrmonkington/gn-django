.. templatefilter:: ljust

``ljust``
---------

Left-aligns the value in a field of a given width.

**Argument:** field size

For example::

    "{{ value|ljust:"10" }}"

If ``value`` is ``Django``, the output will be ``"Django    "``.


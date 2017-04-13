.. templatefilter:: filesizeformat

``filesizeformat``
------------------

Formats the value like a 'human-readable' file size (i.e. ``'13 KB'``,
``'4.1 MB'``, ``'102 bytes'``, etc.).

For example::

    {{ value|filesizeformat }}

If ``value`` is 123456789, the output would be ``117.7 MB``.

.. admonition:: File sizes and SI units

    Strictly speaking, ``filesizeformat`` does not conform to the International
    System of Units which recommends using KiB, MiB, GiB, etc. when byte sizes
    are calculated in powers of 1024 (which is the case here). Instead, Django
    uses traditional unit names (KB, MB, GB, etc.) corresponding to names that
    are more commonly used.


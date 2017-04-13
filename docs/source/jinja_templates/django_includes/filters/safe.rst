.. templatefilter:: safe

``safe``
--------

Marks a string as not requiring further HTML escaping prior to output. When
autoescaping is off, this filter has no effect.

.. note::

    If you are chaining filters, a filter applied after ``safe`` can
    make the contents unsafe again. For example, the following code
    prints the variable as is, unescaped::

        {{ var|safe|escape }}


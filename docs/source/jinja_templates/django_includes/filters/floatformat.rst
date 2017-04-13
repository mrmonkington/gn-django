.. templatefilter:: floatformat

``floatformat``
---------------

When used without an argument, rounds a floating-point number to one decimal
place -- but only if there's a decimal part to be displayed. For example:

============  ===========================  ========
``value``     Template                     Output
============  ===========================  ========
``34.23234``  ``{{ value|floatformat }}``  ``34.2``
``34.00000``  ``{{ value|floatformat }}``  ``34``
``34.26000``  ``{{ value|floatformat }}``  ``34.3``
============  ===========================  ========

If used with a numeric integer argument, ``floatformat`` rounds a number to
that many decimal places. For example:

============  =============================  ==========
``value``     Template                       Output
============  =============================  ==========
``34.23234``  ``{{ value|floatformat:3 }}``  ``34.232``
``34.00000``  ``{{ value|floatformat:3 }}``  ``34.000``
``34.26000``  ``{{ value|floatformat:3 }}``  ``34.260``
============  =============================  ==========

Particularly useful is passing 0 (zero) as the argument which will round the
float to the nearest integer.

============  ================================  ==========
``value``     Template                          Output
============  ================================  ==========
``34.23234``  ``{{ value|floatformat:"0" }}``   ``34``
``34.00000``  ``{{ value|floatformat:"0" }}``   ``34``
``39.56000``  ``{{ value|floatformat:"0" }}``   ``40``
============  ================================  ==========

If the argument passed to ``floatformat`` is negative, it will round a number
to that many decimal places -- but only if there's a decimal part to be
displayed. For example:

============  ================================  ==========
``value``     Template                          Output
============  ================================  ==========
``34.23234``  ``{{ value|floatformat:"-3" }}``  ``34.232``
``34.00000``  ``{{ value|floatformat:"-3" }}``  ``34``
``34.26000``  ``{{ value|floatformat:"-3" }}``  ``34.260``
============  ================================  ==========

Using ``floatformat`` with no argument is equivalent to using ``floatformat``
with an argument of ``-1``.


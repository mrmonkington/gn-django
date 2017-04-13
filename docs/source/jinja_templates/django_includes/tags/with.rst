.. templatetag:: with

``with``
--------

Caches a complex variable under a simpler name. This is useful when accessing
an "expensive" method (e.g., one that hits the database) multiple times.

For example::

    {% with total=business.employees.count %}
        {{ total }} employee{{ total|pluralize }}
    {% endwith %}

The populated variable (in the example above, ``total``) is only available
between the ``{% with %}`` and ``{% endwith %}`` tags.

You can assign more than one context variable::

    {% with alpha=1 beta=2 %}
        ...
    {% endwith %}

.. note:: The previous more verbose format is still supported:
   ``{% with business.employees.count as total %}``

.. _ref-templates-builtins-filters:

Built-in filter reference
=========================


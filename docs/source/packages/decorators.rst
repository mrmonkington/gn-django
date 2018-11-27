.. _gn-django-decorators:

Decorators
==========

``gn_django.decorators`` provides a few reusable decorators.

.. _gn-django-commands-classproperty:

``classproperty``
-----------------

The ``classproperty`` command combines the ``@property`` and ``@classmethod``
decorators to allow a property which can be called directly on a class.

e.g.

.. code:: python

    from gn_django.decorators import classproperty

    class MyClass:

        @classproperty
        def foo(cls):
            return "bar"

    MyClass.foo
    # returns "bar"

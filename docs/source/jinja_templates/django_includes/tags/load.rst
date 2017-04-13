.. templatetag:: load

``load``
--------

Loads a custom template tag set.

For example, the following template would load all the tags and filters
registered in ``somelibrary`` and ``otherlibrary`` located in package
``package``::

    {% load somelibrary package.otherlibrary %}

You can also selectively load individual filters or tags from a library, using
the ``from`` argument. In this example, the template tags/filters named ``foo``
and ``bar`` will be loaded from ``somelibrary``::

    {% load foo bar from somelibrary %}

See :doc:`Custom tag and filter libraries </howto/custom-template-tags>` for
more information.


.. templatetag:: filter

``filter``
----------

Filters the contents of the block through one or more filters. Multiple
filters can be specified with pipes and filters can have arguments, just as
in variable syntax.

Note that the block includes *all* the text between the ``filter`` and
``endfilter`` tags.

Sample usage::

    {% filter force_escape|lower %}
        This text will be HTML-escaped, and will appear in all lowercase.
    {% endfilter %}

.. note::

    The :tfilter:`escape` and :tfilter:`safe` filters are not acceptable
    arguments. Instead, use the :ttag:`autoescape` tag to manage autoescaping
    for blocks of template code.


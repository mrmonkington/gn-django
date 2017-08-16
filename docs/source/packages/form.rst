.. _form-library:

Form
====

General utils
-------------

The following utils can be accessed by importing :code:`gn_django.form.utils`

.. automodule:: gn_django.form.utils
  :members:

Autocomplete
------------

GN Django makes use of the Django Autocomplete Light library to allow to autocomplete
select fields. This library allows select fields to populate from Django querysets.
However, GN Django extends this library to allow for more flexibility, decoupling it
from the Django ORM.

To use, create a view that extends ``gn_django.form.autocomplete.AutocompleteView`` and
assign it to a URL. You will need this for the ``url`` parameter when instanciating
the autocomplete widget.

Override the ``get_option_list()`` method to return a list or tuple of
options. Each option should be either a string, or a dictionary with a ``value`` key
and a ``label`` key.

.. automodule:: gn_django.form.autocomplete

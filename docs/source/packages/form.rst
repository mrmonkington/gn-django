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

This feature relies on two components:

  - A widget render the form field
  - A view to interpret the text entered into the field and return suggestions.

The Widget
~~~~~~~~~~

To use the autocomplete feature, you will need to set the widget in the form to be
an instance of ``gn_django.form.autocomplete.SelectWidget``. This takes the same parameters
as the Django Autocomplete Light widgets, as well as an optional parameter for ``label_finder``.
This is a callable that can be used to find the label that matches the value, if set.

For example::

.. code-block:: python

  from gn_django.form.autocomplete import SelectWidget
  from gravity_core.forms import GravityEditORMForm

  class BlogForm(GravityEditORMForm):
      class Meta:
          def get_label(choice):
              """
              Find blog type that matches given value
              """
              for blog_type in Blog.BLOG_TYPE_CHOICES:
                  if blog_type[0] == choice:
                      return blog_type[1]

          model = Blog
          widgets = {
              'blog_type': SelectWidget(url='autocomplete-blog-types', label_finder=get_label),
          }

In this example, the label for the set value will be determined by looping th rough the ``Blog.BLOG_TYPE_CHOICES`` tuple,
and finding the one that matches.

When the user starts typing, an AJAX request will be made to the view with a name of ``autocomplete-blog-types``,
which will return a JSON response with all the suggestions.

The View
~~~~~~~~

To use, create a view that extends ``gn_django.form.autocomplete.AutocompleteView`` and
assign it to a URL. You will need this for the ``url`` parameter when instanciating
the autocomplete widget (see above).

You will need to override the ``get_option_list()`` method to return a list or tuple of
options. Each option should be either a string, or a dictionary with a ``value`` key
and a ``label`` key. The current user input can be accessed through ``self.q``

Par example::

.. code-block:: python

  from gn_django.form.autocomplete import AutocompleteView

  class BlogTypeAutocompleteView(AutocompleteView):
      def get_option_list(self):
          if not self.q:
              return ()
          pattern = re.compile(r'^%s' % re.escape(self.q), re.IGNORECASE)
          options = []
          for value, label in Blog.BLOG_TYPE_CHOICES:
              if pattern.search(value):
                  options.append({'label': label, 'value': value})

          return tuple(options)

This example checks each of the blog types to see if the current user input
matches the start of the blog type name, and returns all that do.

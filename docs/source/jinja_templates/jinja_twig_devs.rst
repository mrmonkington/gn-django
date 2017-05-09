Jinja for Twig Developers
=========================

Syntactically, Twig and Jinja (and Django templates) are all very similar - they all use
``{{ }}`` for printing, ``{% %}`` for  statements. The key differences lie in minor
syntax details and the names of the expressions, functions and filters.

The follow is a non-exhaustive guide to differences to be aware of when switching between Twig
and Jinja. The full documentation for writing Jinja templates can be found `here <http://jinja.pocoo.org/docs/2.9/templates/>`_.

For loops
---------

Loops in both Twig and Jinja follow the same syntax:

.. code-block:: python

  {% for value in foobar %}
    ...
  {% endfor %}

However, looping through a dictionary is where differences start to appear. Since
in PHP all arrays are treated the same regardless of whether the keys are zero index numbers
or meaningful values, looping through key/value pairs is easy:

.. code-block:: python

  {% for key, value in foobar %}
    ...
  {% endfor %}

In Python, lists, dictionaries and tuples are distinct data structures and Jinja treats
them differently. In Jinja, the syntax above is used to loop through lists of tuples,
where ``key`` is the first item in the tuple and ``value`` is the second

So while the syntax above will work fine for regular lists, with dictionaries it would only loop
through the keys and not the values. The ``items()`` method on the dictionary returns the data
as a list of tuples, with the first item of each being the key, and the second being the value.

Therefore, to loop through key/value pairs, you would need to do this:

.. code-block:: python

  {% for key, value in foobar.items() %}
    ...
  {% endfor %}

The Loop Variable
~~~~~~~~~~~~~~~~~

Twig and Jinja both have a special ``loop`` variable, which holds information about the
current iteration of the loop. However, there are a few differences between sets of information available:

+----------------------------------------+--------------------------------------------+-------------------------------+
| Description                            | Twig                                       | Jinja                         |
+----------------------------------------+--------------------------------------------+-------------------------------+
| The current iteration of the loop      | ``loop.index``                             | ``loop.index``                |
| (1 indexed)                            |                                            |                               |
+----------------------------------------+--------------------------------------------+-------------------------------+
| The current iteration of the loop      | ``loop.index0``                            | ``loop.index0``               |
| (0 indexed)                            |                                            |                               |
+----------------------------------------+--------------------------------------------+-------------------------------+
| The number of iterations from the end  | ``loop.revindex``                          | ``loop.revindex``             |
| of the loop (1 indexed)                |                                            |                               |
+----------------------------------------+--------------------------------------------+-------------------------------+
| The number of iterations from the end  | ``loop.revindex0``                         | ``loop.revindex0``            |
| of the loop (0 indexed)                |                                            |                               |
+----------------------------------------+--------------------------------------------+-------------------------------+
| True if first iteration                | ``loop.first``                             | ``loop.first``                |
+----------------------------------------+--------------------------------------------+-------------------------------+
| True if last iteration                 | ``loop.last``                              | ``loop.last``                 |
+----------------------------------------+--------------------------------------------+-------------------------------+
| The number of items in the sequence    | ``loop.length``                            | ``loop.length``               |
+----------------------------------------+--------------------------------------------+-------------------------------+
| The parent context                     | ``loop.parent``                            | N/A                           |
+----------------------------------------+--------------------------------------------+-------------------------------+
| The depth of the loop (1 indexed)      | N/A                                        | ``loop.depth``                |
+----------------------------------------+--------------------------------------------+-------------------------------+
| The depth of the loop (0 indexed)      | N/A                                        | ``loop.depth0``               |
+----------------------------------------+--------------------------------------------+-------------------------------+
| Cycle through arbitrary variables      | ``cycle(['odd', 'even'], loop.index0)``    | ``loop.cycle('odd', 'even')`` |
| depending on the iteration             |                                            |                               |
+----------------------------------------+--------------------------------------------+-------------------------------+

If statements
-------------

If statements are largely the same in Jinja as they are in Twig, with the only major difference
being that Jinja uses the Pythonic ``elif`` instead of ``elseif``.

Macros
------

Macros are similar in Jinja to Twig, with the big exception being that Jinja macros support
named parameters. If they exist in the same template, they do not need to be imported
or called from ``_self``.

This means that you can do this:

.. code-block:: python

  {% macro do_a_thing(foo='moo', bar='baz') %}
    <p>Doing a thing with {{ foo }} and {{ bar }}</p>
  {% endmacro %}

  {{ do_a_thing('woo') }}
  {{ do_a_thing(bar='duck') }}

So the above would output:

.. code-block:: html

  <p>Doing a thing with woo and baz</p>
  <p>Doing a thing with moo and duck</p>

It is also possible to import specific macros from an external templates and assign them
to an alias:

.. code-block:: python

  {% from 'macros.html' import mormont as mmt, yafa %}
  {{ mmt() }}
  {{ yafa() }}

This would import a macro called ``mormont()`` and alias it to ``mmt()``, and also import
a macro called ``yafa()``.

Includes
--------

Out of the box, Jinja's ``include`` statements are more limited that Twig's. Where Twig allows
you to send variables to the context of the included template, with or without the wider context,
Jinja only allows to include or exclude the entire context. To alias variables to match those
in the context, you must use the cumbersome ``with`` feature:

.. code-block:: python

  {% with foo = 'hello' %}
    {% with bar = 'world' %}
      {% include 'helloworld.html' with context %}
    {% endwith %}
  {% endwith %}

Fortunately, we also have...

Include With
~~~~~~~~~~~~

GN Django comes with a Jinja extension bringing in an ``include_with`` tag. This allows for
the context to be easily redefined within a single statement:

.. code-block:: python

  {% include_with 'helloworld.html' foo='hello', bar='world' %}

**Note:** This tag completely redeclares the context, so the only values that will be sent
to ``helloworld.html`` will be ``foo`` and ``bar``. No variables declared in the view
or in any context processors will be sent unless explicitly declared.

Whitespace
----------

Jinja does not come with ``spaceless`` tags out of the box. However it has been included
as part of the GN Django library. Jinja also supports ``{%- -%}`` tags to remove whitespace.
For more information, view the `official Jinja documentation <http://jinja.pocoo.org/docs/2.9/templates/#whitespace-control>`_.

JSON Encoding
-------------

Twig duplicates PHP's own `json_encode()` function. To convert data to a JSON format in
Jinja, you need to use the `tojson()` filter:

.. code-block:: python

  {{ some_data|tojson }}

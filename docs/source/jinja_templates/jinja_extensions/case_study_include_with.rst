Case Study: Writing the 'Include With' Jinja extension
======================================================

Overview
--------

This article discusses the process of developing the ``IncludeWithExtension``. The brief
was to create an extension that would allow developers to easily include templates
without having to use the cumbersome syntax of Jinja's own `With` feature:

.. code-block:: jinja2

  {% with 'foo' as bar %}
  	{% with 'hello' as world %}
  		{% include 'somefile.html' with context %}
  	{% endwith %}
  {% endwith %}

We wanted something closer to Twig's implementation, where the included template
has its own context and this can be defined by within the include statement. Since
we don't want to overwrite the existing ``include`` statement, this is called using
an ``include_with`` tag, so the above statement would look like this:

.. code-block:: jinja2

  {% include_with 'somefile.html' bar='foo', world='hello' %}

In this example, the *only* variables in the context for ``somefile.html`` are those
defined in the ``include_with`` statement (as well as any automatically included by
the context processors).

Accessing the context
---------------------

**Note:** All classes referenced below exist within the ``jinja2`` namespace unless
stated otherwise.

The main thing causing issues when trying to write the ``include_with`` extension
was accessing the context of the current template to pass variables to the included
template. This issue was one of basic understanding of how Jinja extensions work.
Essentially, the template **does not** have access to the context, all it can store
are references to items in the context. Context variables can only be accessed in callbacks,
which are defined as part of the extension class and called using the base `ext.Extension`
class' ``call_method`` method.

I found that this was only useful when wrapped in a ``nodes.CallBlock`` class as well.

My ``parse()`` method ended up very small and looked like this:

.. code-block:: python

    def parse(self, parser):

        # First part will be 'include_with' tag, but also contains line number which
        # we use
        first = parser.parse_expression()

        # Second part is the template name
        template = parser.parse_expression()

        # Grab the context variables
        cvars = self._get_params(parser)

        call = self.call_method('_render', [template, cvars], lineno=first.lineno)

        return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

The ``cvars`` variable is an instance of ``nodes.Dict``, which acts as a representation
of a dictionary. Within this class is a `list` of ``nodes.Pair`` instances. The ``nodes.Pair``
class is a key/value pair, which each key being a ``nodes.Const`` instance, and each
value being either a ``nodes.Name`` instance, or a node extending ``nodes.Literal``.
``nodes.Literal`` objects represent a constant/hardcoded value. ``nodes.Name`` objects
represent a reference to a variable stored in the context.

When ``cvars`` is filtered through ``self.call_method()``, it is converted into a dictionary
of values, with ``nodes.Const`` instances becoming the hardcoded value they represent,
and ``nodes.Name`` instances pulling the value from the context.

This means that if our view looks like this:

.. code-block:: python

  {% set hello = 'world' %}
  {% include_with 'include.html' foo=['bar'], baz=hello %}

Within the scope of the ``parse()`` method, ``cvars`` will look like this (simplified):

.. code-block::

  nodes.Dict:
  	- nodes.Pair(
  		key: nodes.Const(value='foo'),
  		value: nodes.Const(value=['bar'])
  	),
  	- nodes.Pair(
  		key: nodes.Const(value='baz'),
  		value: nodes.Name(name='hello')
  	)

Once this ``nodes.Dict`` is sent passed through ``self.call_method()``, it will be a
simple dictionary, where ``hello`` has been replaced by its variable in the context,
``world``:

.. code-block:: python

  {
  	'foo': ['bar'],
  	'baz': 'world',
  }

The ``self._render()`` method then takes these variables and renders the included
template using this dictionary as the context:

.. code-block:: python

    def _render(self, template, cvars, caller):
        return self.environment.get_template(template).render(cvars)

Finally, the method returns an instance of ``nodes.CallBlock``, which acts as a
macro to output a string returned by the `call` variable (in this case the returned
value of ``self._render``). All the nodes are quite fussy about being passed the correct
number of variables, which is a bit of a pain as often they will be empty. The three
empty lists passed to ``nodes.CallBlock`` represent ``args``, ``defaults`` and ``body``, and
I don't know what they do.

Returning ``call`` itself will causing a confusing syntax error on a line that may
not exist in the view. The reason for this is that the syntax error is actually
appearing in the template *after* it's been compiled into Python code, and returning
some nodes will cause it to inject weird syntax into method parameters.

The ``nodes.ContextReference`` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While it ended up not being necessary, another way to access context variables is
using the ``nodes.ContextReference`` class. The class is useless on its own, but when
filtered through ``self.call_method()`` gets swapped out for the an instance of
``runtime.Context`` - an iterable object storing the context variables.

Therefore, if you wanted to access a variable ``foo`` in the context, you would need
to write something like this:

.. code-block:: python

  def parse(self, parser):
  	first = parser.parse_expression()
  	ctx = nodes.ContextReference()
  	call = self.call_method('_get_foo', [ctx], lineno=first.lineno)

  	return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

  def _get_foo(self, ctx, caller):
  	# `ctx` is now an instance of runtime.Context
  	return ctx['foo']

Parsing the statement
---------------------

The ``lexer.TokenStream`` class is an generator that returns each section of the
statement declared in the template. This is used by the ``jinja.parser.Parser``
class which interprets the tokens and converts them into nodes. The token stream is
accessed via ``parser.stream`` in the ``parse()`` method.

The first two variables shown by the stream are the ``include_with`` tag itself
(represented as a ``nodes.Name`` instance), and the second is the template name
(represented as a ``nodes.Const`` instance, as it is a string). Once those two have
been declared, we need to pull the variables from the stream with the following
method (which is largely adapted from `this <https://github.com/coffin/coffin/blob/master/coffin/common.py#L164
`_):

.. code-block:: python

    def _get_params(self, parser):
        stream = parser.stream
        kwargs = []
        eval_ctx = nodes.EvalContext(self.environment)
        while not stream.current.test_any('block_end'):
            stream.skip_if('comma')
            if stream.current.test('name') and stream.look().test('assign'):
                key = nodes.Const(next(stream).value)
                stream.skip()
                value = parser.parse_expression()
                kwargs.append(nodes.Pair(key, value, lineno=key.lineno))

        kwargs = nodes.Dict(kwargs)

        return kwargs

This method loops through the stream until it reaches the end (represented by ``block_end``).
It checks for variable names (``name``) followed by an equals sign (``assign``). Upon
finding this, it will call ``parser.parse_expression()`` to get an instance of either
``nodes.Const`` or ``nodes.Name``, and assign both to a ``nodes.Pair``. Once it has finished
checking the stream, it sends the list of ``nodes.Pair`` instances to a ``nodes.Dict``
instance and returns it.

The token stream is actually `quite well documented <http://jinja.pocoo.org/docs/2.9/extensions/#jinja2.lexer.TokenStream>`_
and is full of simple, relatively easy to understand methods for observing and
traversing the stream. The various different tokens are declared `in the source code <https://github.com/pallets/jinja/blob/059fbe5c0085a52efb63fe8076f9c53e811aa30a/jinja2/lexer.py#L64>`_.

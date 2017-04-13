Using Jinja templates
=====================

Here's how the official jinja documentation describes itself:

    "A Jinja template is simply a text file. 
    Jinja can generate any text-based format (HTML, XML, CSV, LaTeX, etc.). A 
    Jinja template doesn’t need to have a specific extension: .html, .xml, or 
    any other extension is just fine.

    A template contains variables and/or expressions, which get replaced with 
    values when a template is rendered; and tags, which control the logic of 
    the template. The template syntax is heavily inspired by Django and Python."


To get up to speed on the syntax and semantics of Jinja templates, refer to
the documentation here: http://jinja.pocoo.org/docs/2.9/templates/.

The following reference documentation assumes that you know the general syntax
of jinja.  gn-django offers an extended jinja library and the following 
reference documentation *should* provide an exhaustive reference of: 
- filters 
- globals 
- tests
- extensions
- context processors - what they are, and how to use them
- custom template loaders

.. include:: filters.rst

Filters reference
-----------------

Vanilla Jinja Filters
~~~~~~~~~~~~~~~~~~~~~

.. jinjafilters::

Django Filters (from django-jinja)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: addslashes(value)

    Adds slashes before quotes. Useful for escaping strings in CSV, for example.
    
    For example::
    
        {{ value|addslashes }}
    
    If ``value`` is ``"I'm using Django"``, the output will be
    ``"I\'m using Django"``.

.. function:: capfirst(value)

    Capitalizes the first character of the value. If the first character is not
    a letter, this filter has no effect.
    
    For example::
    
        {{ value|capfirst }}
    
    If ``value`` is ``"django"``, the output will be ``"Django"``.

.. function:: escapejs(value)

    Escapes characters for use in JavaScript strings. This does *not* make the
    string safe for use in HTML, but does protect you from syntax errors when using
    templates to generate JavaScript/JSON.
    
    For example::
    
        {{ value|escapejs }}
    
    If ``value`` is ``"testing\r\njavascript \'string" <b>escaping</b>"``,
    the output will be ``"testing\\u000D\\u000Ajavascript \\u0027string\\u0022 \\u003Cb\\u003Eescaping\\u003C/b\\u003E"``.

.. function:: floatformat(value)

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


.. function:: iriencode(value)

    Converts an IRI (Internationalized Resource Identifier) to a string that is
    suitable for including in a URL. This is necessary if you're trying to use
    strings containing non-ASCII characters in a URL.
    
    It's safe to use this filter on a string that has already gone through the
    :tfilter:`urlencode` filter.
    
    For example::
    
        {{ value|iriencode }}
    
    If ``value`` is ``"?test=1&me=2"``, the output will be ``"?test=1&amp;me=2"``.


.. function:: linenumbers(value)

    Displays text with line numbers.
    
    For example::
    
        {{ value|linenumbers }}
    
    If ``value`` is::
    
        one
        two
        three
    
    the output will be::
    
        1. one
        2. two
        3. three


.. function:: makelist(value)

    Returns the value turned into a list. For a string, it's a list of characters.
    For an integer, the argument is cast to a string before creating a list.
    
    For example::
    
        {{ value|make_list }}
    
    If ``value`` is the string ``"Joel"``, the output would be the list
    ``['J', 'o', 'e', 'l']``. If ``value`` is ``123``, the output will be the
    list ``['1', '2', '3']``.


.. function:: slugify(s)

    Converts to ASCII. Converts spaces to hyphens. Removes characters that aren't
    alphanumerics, underscores, or hyphens. Converts to lowercase. Also strips
    leading and trailing whitespace.
    
    For example::
    
        {{ value|slugify }}
    
    If ``value`` is ``"Joel is a slug"``, the output will be ``"joel-is-a-slug"``.


.. function:: stringformat(s, format)

    Formats the variable according to the argument, a string formatting specifier.
    This specifier uses the :ref:`old-string-formatting` syntax, with the exception
    that the leading "%" is dropped.
    
    For example::
    
        {{ value|stringformat("E") }}
    
    If ``value`` is ``10``, the output will be ``1.000000E+01``.


.. function:: truncatechars(s, length)

    Truncates a string if it is longer than the specified number of characters.
    Truncated strings will end with a translatable ellipsis sequence ("...").
    
    **Argument:** Number of characters to truncate to
    
    For example::
    
        {{ value|truncatechars(9) }}
    
    If ``value`` is ``"Joel is a slug"``, the output will be ``"Joel i..."``.


.. function:: truncatechars_html(s, length)

    Similar to :tfilter:`truncatechars`, except that it is aware of HTML tags. Any
    tags that are opened in the string and not closed before the truncation point
    are closed immediately after the truncation.
    
    For example::
    
        {{ value|truncatechars_html(9) }}
    
    If ``value`` is ``"<p>Joel is a slug</p>"``, the output will be
    ``"<p>Joel i...</p>"``.

    Newlines in the HTML content will be preserved.


.. function:: truncatewords(s, words)

    Truncates a string after a certain number of words.

    **Argument:** Number of words to truncate after
    
    For example::
    
        {{ value|truncatewords(2) }}
    
    If ``value`` is ``"Joel is a slug"``, the output will be ``"Joel is ..."``.
    
    Newlines within the string will be removed.


.. function:: truncatewords_html(s, words)

    Similar to :tfilter:`truncatewords`, except that it is aware of HTML tags. Any
    tags that are opened in the string and not closed before the truncation point,
    are closed immediately after the truncation.
    
    This is less efficient than :tfilter:`truncatewords`, so should only be used
    when it is being passed HTML text.
    
    For example::
    
        {{ value|truncatewords_html:2 }}
    
    If ``value`` is ``"<p>Joel is a slug</p>"``, the output will be
    ``"<p>Joel is ...</p>"``.
    
    Newlines in the HTML content will be preserved.


.. function:: urlizetrunc(s, length)

    Converts URLs and email addresses into clickable links just like urlize_, but
    truncates URLs longer than the given character limit.
    
    **Argument:** Number of characters that link text should be truncated to,
    including the ellipsis that's added if truncation is necessary.
    
    For example::
    
        {{ value|urlizetrunc:15 }}
    
    If ``value`` is ``"Check out www.djangoproject.com"``, the output would be
    ``'Check out <a href="http://www.djangoproject.com"
    rel="nofollow">www.djangopr...</a>'``.
    
    As with urlize_, this filter should only be applied to plain text.


.. function:: ljust(s, size)

    Left-aligns the value in a field of a given width.

    **Argument:** field size
    
    For example::
    
        "{{ value|ljust:"10" }}"
    
    If ``value`` is ``Django``, the output will be ``"Django    "``.


.. function:: rjust(s, size)

    Right-aligns the value in a field of a given width.

    **Argument:** field size
    
    For example::
    
        "{{ value|rjust:"10" }}"
    
    If ``value`` is ``Django``, the output will be ``"    Django"``.




Tests reference
---------------

.. jinjatests::

Globals reference
-----------------

.. function:: range([start,] stop[, step])

    Return a list containing an arithmetic progression of integers.
    ``range(i, j)`` returns ``[i, i+1, i+2, ..., j-1]``;
    start (!) defaults to ``0``.
    When step is given, it specifies the increment (or decrement).
    For example, ``range(4)`` and ``range(0, 4, 1)`` return ``[0, 1, 2, 3]``.
    The end point is omitted!
    These are exactly the valid indices for a list of 4 elements.

    This is useful to repeat a template block multiple times, e.g.
    to fill a list.  Imagine you have 7 users in the list but you want to
    render three empty items to enforce a height with CSS::

        <ul>
        {% for user in users %}
            <li>{{ user.username }}</li>
        {% endfor %}
        {% for number in range(10 - users|count) %}
            <li class="empty"><span>...</span></li>
        {% endfor %}
        </ul>

.. function:: lipsum(n=5, html=True, min=20, max=100)

    Generates some lorem ipsum for the template.  By default, five paragraphs
    of HTML are generated with each paragraph between 20 and 100 words.
    If html is False, regular text is returned.  This is useful to generate simple
    contents for layout testing.

.. function:: dict(\**items)

    A convenient alternative to dict literals.  ``{'foo': 'bar'}`` is the same
    as ``dict(foo='bar')``.

.. class:: cycler(\*items)

    The cycler allows you to cycle among values similar to how `loop.cycle`
    works.  Unlike `loop.cycle`, you can use this cycler outside of
    loops or over multiple loops.

    This can be very useful if you want to show a list of folders and
    files with the folders on top but both in the same list with alternating
    row colors.

    The following example shows how `cycler` can be used::

        {% set row_class = cycler('odd', 'even') %}
        <ul class="browser">
        {% for folder in folders %}
          <li class="folder {{ row_class.next() }}">{{ folder|e }}</li>
        {% endfor %}
        {% for filename in files %}
          <li class="file {{ row_class.next() }}">{{ filename|e }}</li>
        {% endfor %}
        </ul>

    A cycler has the following attributes and methods:

    .. method:: reset()

        Resets the cycle to the first item.

    .. method:: next()

        Goes one item ahead and returns the then-current item.

    .. attribute:: current

        Returns the current item.

    **new in Jinja 2.1**

.. class:: joiner(sep=', ')

    A tiny helper that can be used to "join" multiple sections.  A joiner is
    passed a string and will return that string every time it's called, except
    the first time (in which case it returns an empty string).  You can
    use this to join things::

        {% set pipe = joiner("|") %}
        {% if categories %} {{ pipe() }}
            Categories: {{ categories|join(", ") }}
        {% endif %}
        {% if author %} {{ pipe() }}
            Author: {{ author() }}
        {% endif %}
        {% if can_edit %} {{ pipe() }}
            <a href="?action=edit">Edit</a>
        {% endif %}

    **new in Jinja 2.1**

Extensions reference
--------------------

Expression Statement
~~~~~~~~~~~~~~~~~~~~

If the expression-statement extension is loaded, a tag called `do` is available
that works exactly like the regular variable expression (``{{ ... }}``); except
it doesn't print anything.  This can be used to modify lists::

    {% do navigation.append('a string') %}


Loop Controls
~~~~~~~~~~~~~

If the application enables the :ref:`loopcontrols-extension`, it's possible to
use `break` and `continue` in loops.  When `break` is reached, the loop is
terminated;  if `continue` is reached, the processing is stopped and continues
with the next iteration.

Here's a loop that skips every second item::

    {% for user in users %}
        {%- if loop.index is even %}{% continue %}{% endif %}
        ...
    {% endfor %}

Likewise, a loop that stops processing after the 10th iteration::

    {% for user in users %}
        {%- if loop.index >= 10 %}{% break %}{% endif %}
    {%- endfor %}

Note that ``loop.index`` starts with 1, and ``loop.index0`` starts with 0
(See: :ref:`for-loop`).


With Statement
~~~~~~~~~~~~~~

.. versionadded:: 2.3

If the application enables the :ref:`with-extension`, it is possible to
use the `with` keyword in templates.  This makes it possible to create
a new inner scope.  Variables set within this scope are not visible
outside of the scope.

With in a nutshell::

    {% with %}
        {% set foo = 42 %}
        {{ foo }}           foo is 42 here
    {% endwith %}
    foo is not visible here any longer

Because it is common to set variables at the beginning of the scope,
you can do that within the `with` statement.  The following two examples
are equivalent::

    {% with foo = 42 %}
        {{ foo }}
    {% endwith %}

    {% with %}
        {% set foo = 42 %}
        {{ foo }}
    {% endwith %}

.. _autoescape-overrides:

Autoescape Extension
~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.4

If the application enables the :ref:`autoescape-extension`, one can
activate and deactivate the autoescaping from within the templates.

Example::

    {% autoescape true %}
        Autoescaping is active within this block
    {% endautoescape %}

    {% autoescape false %}
        Autoescaping is inactive within this block
    {% endautoescape %}

After an `endautoescape` the behavior is reverted to what it was before.

Context processors
------------------


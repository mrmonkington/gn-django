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

Filters reference
-----------------

Vanilla Jinja Filters
~~~~~~~~~~~~~~~~~~~~~

.. jinjafilters::

Django Filters (from django-jinja)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: django_includes/filters/addslashes.rst

.. include:: django_includes/filters/capfirst.rst

.. include:: django_includes/filters/escapejs.rst

.. include:: django_includes/filters/floatformat.rst

.. include:: django_includes/filters/iriencode.rst

.. include:: django_includes/filters/linenumbers.rst

.. include:: django_includes/filters/make_list.rst

.. include:: django_includes/filters/slugify.rst

.. include:: django_includes/filters/stringformat.rst

.. include:: django_includes/filters/truncatechars.rst

.. include:: django_includes/filters/truncatechars_html.rst

.. include:: django_includes/filters/truncatewords.rst

.. include:: django_includes/filters/truncatewords_html.rst

.. include:: django_includes/filters/urlizetrunc.rst

.. include:: django_includes/filters/ljust.rst

.. include:: django_includes/filters/cut.rst

.. include:: django_includes/filters/linebreaksbr.rst

.. include:: django_includes/filters/linebreaks.rst

.. include:: django_includes/filters/striptags.rst

.. include:: django_includes/filters/add.rst

.. include:: django_includes/filters/date.rst

.. include:: django_includes/filters/time.rst

.. include:: django_includes/filters/timesince.rst

.. include:: django_includes/filters/timeuntil.rst

.. include:: django_includes/filters/default_if_none.rst

.. include:: django_includes/filters/divisibleby.rst

.. include:: django_includes/filters/yesno.rst

.. include:: django_includes/filters/pluralize.rst

.. include:: django_includes/filters/localtime.rst

.. include:: django_includes/filters/utc.rst

.. include:: django_includes/filters/timezone.rst

.. include:: django_includes/filters/apnumber.rst

.. include:: django_includes/filters/intcomma.rst

.. include:: django_includes/filters/intword.rst

.. include:: django_includes/filters/naturalday.rst

.. include:: django_includes/filters/naturaltime.rst

.. include:: django_includes/filters/ordinal.rst

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

.. function:: url(name, **url_kwargs)

    Url reversal function which allows templates to refer to named Urls.

    Reverse urls in templates::

        {{ url('ns:name', pk=obj.pk) }}
    
    This approach is very flexible, because we do not need additional options 
    to set a result if executing url in one variable. With jinja2 you can use 
    the set template tag for it::

        {% set myurl=url("ns:name", pk=obj.pk) %}


.. function:: static(filename)

    To link to static files that are saved in ``STATIC_ROOT`` the 
    `static` global is used. If the `django.contrib.staticfiles`
    app is installed, the tag will serve files using ``url()`` method of the
    storage specified by the ``STATICFILES_STORAGE`` setting. For example::

        {{ static("js/lib/foo.js") }}
    

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

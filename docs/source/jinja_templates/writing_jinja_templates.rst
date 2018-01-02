Writing Jinja templates - reference docs
========================================

Here's how the official jinja documentation describes itself:

    "A Jinja template is simply a text file.

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
    - custom template loaders

File extension
--------------

The Jinja2 project does not mandate that any particular file extension is used
for jinja template files.  However, the agreed standard for Gamer Network django
projects is to use the ``.j2`` extension.

By default, the gn-django jinja2 backend class (``gn_django.template.backend.Jinja2"``)
will only be used for templates named with the ``.j2`` extension e.g. ``home.j2``.

The reasons for settling on ``.j2`` are as follows:

  * It allows us to use the ``match_extension`` option for the django-jinja
    backend.  This means that the template backend will relinquish rendering
    for template names that do not end in ``.j2`` - so in theory we could use
    django templating in addition to jinja if we needed to.
  * It matches ansible - which requires that template files end with ``.j2``.
  * Syntax highlighting can be easily set for editors, based on file extension.
  * Generally, many open source projects use some sort of file extension for
    jinja templates.  ``.jinja`` is too long.  ``.html.j2`` is annoying.
    ``.j2`` is juuust right.


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

.. function:: randint(maximum=100, minimum=0)

    Generate and print a random number between the ``minimum`` and ``maximum`` value.

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

.. _include-with-statement:

Include With Statement
~~~~~~~~~~~~~~~~~~~~~~

This is a GN specific extension that allows developer to include templates
with a redeclared context. This is done using the ``include_with``, followed by
the name of the template, and then keyword arguments separated by commas. This negates
the need to use the :ref:`With statement <with-statement>` when using includes.

**Note:** This will completely override the current context,
meaning that any variables declared by context processors *will not* be included in
the context of the included template. For more information, read the :ref:`case study <gn-django-writing-include-with-ext>`

Example::

    {% include_with 'subtemplate.j2' foo='bar', key=['value'] %}

.. _with-statement:

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

.. _gn-django-static-link:

Static Link Extension
~~~~~~~~~~~~~~~~~~~~~

This is a GN specific extension to aid development with static file linking and precompilation.
The purpose is to allow different files to be linked to in different development
environments. In a dev environment, it may be beneficial to link to a ``LESS`` file rather than
a ``CSS`` file, for example.

The following tags come included with the extension:

- ``{% css '[name]' %}`` - Link to a stylesheet. The ``name`` is the file path within the static directory for that file type, without a file extension e.g. ``pages/article``
- ``{% js '[name]' %}`` - Link to a JavaScript file. The ``name`` is the file path within the static directory for that file type, without a file extension e.g. ``pages/article`
- ``{% load_compilers %}`` - Link to compiler scripts for client-side compilation of static files when in a dev environment (outputs nothing in production).

The extension is highly configurable:

- ``STATICLINK_PREPROCESSORS`` - A dictionary mapping script type to preprocessors::

    STATICLINK_PREPROCESSORS = {
      'css': 'less',
    }
- ``STATICLINK_CLIENT_COMPILERS`` - A dictionary mapping script type to the URLs or client-side compilation scripts::

    STATICLINK_CLIENT_COMPILERS = {
        'css': '//cdnjs.cloudflare.com/ajax/libs/less.js/2.7.1/less.min.js',
    }

- ``STATICLINK_DEBUG`` - This option allows you to enable or disable debug mode for different script types::

    STATICLINK_DEBUG = {
       'css': False,
       'js': True,
    }

- ``STATICLINK_FILE_MAP`` - A dictionary mapping file extensions to directory. If it is not set, it will default to a directory of the same name as the file extension::

    STATICLINK_FILE_MAP = {
       'js': 'scripts',
       'less': 'precompiled',
    }

- ``STATICLINK_VERSION`` - A unique version number to append to the static file URLs for cache-busting. Defaults to "latest".

As example of this in action can be found in the ``simple`` example with the ``static-link-extnesion`` slug.

The template has the following in the header::

  {% css 'test' %}
  {% js 'test' %}
  {% load_compilers %}

In debug mode, this is output::

  <link href="/static/less/test.less?v=1497282637.059254" rel="stylesheet" type="text/less" />
  <script src="/static/scripts/test.js?v=1497282637.0611155" type="application/javascript"></script>

  <script src="//cdnjs.cloudflare.com/ajax/libs/less.js/2.7.1/less.min.js"></script>
  <script>localStorage.clear();</script>

While in production, this is output::

  <link href="/static/css/test.css?v=1497350630.0394886" rel="stylesheet" type="text/css" />
  <script src="/static/js/test.js?v=1497350630.0409005" type="application/javascript"></script>

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

CSRF Extension
~~~~~~~~~~~~~~

This provides protection against cross site request forgeries, as described
`in the django documentation <https://docs.djangoproject.com/en/dev/ref/csrf/>`_.

Example::

    <form action="" method="post">
        {% csrf_token %}
        ...
    </form>1

.. templatetag:: include

.. function:: include

    Loads a template and renders it with the current context. This is a way of
    "including" other templates within a template.
    
    The template name can either be a variable or a hard-coded (quoted) string,
    in either single or double quotes.
    
    This example includes the contents of the template ``"foo/bar.html"``::
    
        {% include "foo/bar.html" %}
    
    A string argument may be a relative path starting with ``./`` or ``../`` as
    described in the :ttag:`extends` tag.
    
    This example includes the contents of the template whose name is contained in
    the variable ``template_name``::
    
        {% include template_name %}
    
    The variable may also be any object with a ``render()`` method that accepts a
    context. This allows you to reference a compiled ``Template`` in your context.
    
    An included template is rendered within the context of the template that
    includes it. This example produces the output ``"Hello, John!"``:
    
    * Context: variable ``person`` is set to ``"John"`` and variable ``greeting``
      is set to ``"Hello"``.
    
    * Template::
    
        {% include "name_snippet.html" %}
    
    * The ``name_snippet.html`` template::
    
        {{ greeting }}, {{ person|default:"friend" }}!
    
    You can pass additional context to the template using keyword arguments::
    
        {% include "name_snippet.html" with person="Jane" greeting="Hello" %}
    
    If you want to render the context only with the variables provided (or even
    no variables at all), use the ``only`` option. No other variables are
    available to the included template::
    
        {% include "name_snippet.html" with greeting="Hi" only %}
    
    If the included template causes an exception while it's rendered (including
    if it's missing or has syntax errors), the behavior varies depending on the
    :class:`template engine's <django.template.Engine>` ``debug`` option (if not
    set, this option defaults to the value of :setting:`DEBUG`). When debug mode is
    turned on, an exception like :exc:`~django.template.TemplateDoesNotExist` or
    :exc:`~django.template.TemplateSyntaxError` will be raised. When debug mode
    is turned off, ``{% include %}`` logs a warning to the ``django.template``
    logger with the exception that happens while rendering the included template
    and returns an empty string.
    
    .. deprecated:: 1.11
    
        Silencing exceptions raised while rendering the ``{% include %}`` template
        tag is deprecated. In Django 2.1, the exception will be raised.
    
    .. note::
        The :ttag:`include` tag should be considered as an implementation of
        "render this subtemplate and include the HTML", not as "parse this
        subtemplate and include its contents as if it were part of the parent".
        This means that there is no shared state between included templates --
        each include is a completely independent rendering process.
    
        Blocks are evaluated *before* they are included. This means that a template
        that includes blocks from another will contain blocks that have *already
        been evaluated and rendered* - not blocks that can be overridden by, for
        example, an extending template.
    
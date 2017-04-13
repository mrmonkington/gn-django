.. templatetag:: firstof

``firstof``
-----------

Outputs the first argument variable that is not ``False``. Outputs nothing if
all the passed variables are ``False``.

Sample usage::

    {% firstof var1 var2 var3 %}

This is equivalent to::

    {% if var1 %}
        {{ var1 }}
    {% elif var2 %}
        {{ var2 }}
    {% elif var3 %}
        {{ var3 }}
    {% endif %}

You can also use a literal string as a fallback value in case all
passed variables are False::

    {% firstof var1 var2 var3 "fallback value" %}

This tag auto-escapes variable values. You can disable auto-escaping with::

    {% autoescape off %}
        {% firstof var1 var2 var3 "<strong>fallback value</strong>" %}
    {% endautoescape %}

Or if only some variables should be escaped, you can use::

    {% firstof var1 var2|safe var3 "<strong>fallback value</strong>"|safe %}

You can use the syntax ``{% firstof var1 var2 var3 as value %}`` to store the
output inside a variable.


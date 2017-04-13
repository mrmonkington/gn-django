.. templatetag:: for

``for``
-------

Loops over each item in an array, making the item available in a context
variable. For example, to display a list of athletes provided in
``athlete_list``::

    <ul>
    {% for athlete in athlete_list %}
        <li>{{ athlete.name }}</li>
    {% endfor %}
    </ul>

You can loop over a list in reverse by using
``{% for obj in list reversed %}``.

If you need to loop over a list of lists, you can unpack the values
in each sublist into individual variables. For example, if your context
contains a list of (x,y) coordinates called ``points``, you could use the
following to output the list of points::

    {% for x, y in points %}
        There is a point at {{ x }},{{ y }}
    {% endfor %}

This can also be useful if you need to access the items in a dictionary.
For example, if your context contained a dictionary ``data``, the following
would display the keys and values of the dictionary::

    {% for key, value in data.items %}
        {{ key }}: {{ value }}
    {% endfor %}

Keep in mind that for the dot operator, dictionary key lookup takes precedence
over method lookup. Therefore if the ``data`` dictionary contains a key named
``'items'``, ``data.items`` will return ``data['items']`` instead of
``data.items()``. Avoid adding keys that are named like dictionary methods if
you want to use those methods in a template (``items``, ``values``, ``keys``,
etc.). Read more about the lookup order of the dot operator in the
:ref:`documentation of template variables <template-variables>`.

The for loop sets a number of variables available within the loop:

==========================  ===============================================
Variable                    Description
==========================  ===============================================
``forloop.counter``         The current iteration of the loop (1-indexed)
``forloop.counter0``        The current iteration of the loop (0-indexed)
``forloop.revcounter``      The number of iterations from the end of the
                            loop (1-indexed)
``forloop.revcounter0``     The number of iterations from the end of the
                            loop (0-indexed)
``forloop.first``           True if this is the first time through the loop
``forloop.last``            True if this is the last time through the loop
``forloop.parentloop``      For nested loops, this is the loop surrounding
                            the current one
==========================  ===============================================

``for`` ... ``empty``
---------------------

The ``for`` tag can take an optional ``{% empty %}`` clause whose text is
displayed if the given array is empty or could not be found::

    <ul>
    {% for athlete in athlete_list %}
        <li>{{ athlete.name }}</li>
    {% empty %}
        <li>Sorry, no athletes in this list.</li>
    {% endfor %}
    </ul>

The above is equivalent to -- but shorter, cleaner, and possibly faster
than -- the following::

    <ul>
      {% if athlete_list %}
        {% for athlete in athlete_list %}
          <li>{{ athlete.name }}</li>
        {% endfor %}
      {% else %}
        <li>Sorry, no athletes in this list.</li>
      {% endif %}
    </ul>


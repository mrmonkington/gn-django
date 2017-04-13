.. templatetag:: regroup

.. function:: regroup

    Regroups a list of alike objects by a common attribute.
    
    This complex tag is best illustrated by way of an example: say that ``cities``
    is a list of cities represented by dictionaries containing ``"name"``,
    ``"population"``, and ``"country"`` keys:
    
    .. code-block:: python
    
        cities = [
            {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
            {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
            {'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
            {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
            {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
        ]
    
    ...and you'd like to display a hierarchical list that is ordered by country,
    like this:
    
    * India
    
      * Mumbai: 19,000,000
      * Calcutta: 15,000,000
    
    * USA
    
      * New York: 20,000,000
      * Chicago: 7,000,000
    
    * Japan
    
      * Tokyo: 33,000,000
    
    You can use the ``{% regroup %}`` tag to group the list of cities by country.
    The following snippet of template code would accomplish this::
    
        {% regroup cities by country as country_list %}
    
        <ul>
        {% for country in country_list %}
            <li>{{ country.grouper }}
            <ul>
                {% for city in country.list %}
                  <li>{{ city.name }}( {{ city.population) }}</li>
                {% endfor %}
            </ul>
            </li>
        {% endfor %}
        </ul>
    
    Let's walk through this example. ``{% regroup %}`` takes three arguments: the
    list you want to regroup, the attribute to group by, and the name of the
    resulting list. Here, we're regrouping the ``cities`` list by the ``country``
    attribute and calling the result ``country_list``.
    
    ``{% regroup %}`` produces a list (in this case, ``country_list``) of
    **group objects**. Group objects are instances of
    :py:func:`~collections.namedtuple` with two fields:
    
    * ``grouper`` -- the item that was grouped by (e.g., the string "India" or
      "Japan").
    * ``list`` -- a list of all items in this group (e.g., a list of all cities
      with country='India').
    
    .. versionchanged:: 1.11
    
        The group object was changed from a dictionary to a
        :py:func:`~collections.namedtuple`.
    
    Because ``{% regroup %}`` produces :py:func:`~collections.namedtuple` objects,
    you can also write the previous example as::
    
        {% regroup cities by country as country_list %}
    
        <ul>
        {% for country, local_cities in country_list %}
            <li>{{ country }}
            <ul>
                {% for city in local_cities %}
                  <li>{{ city.name }}( {{ city.population) }}</li>
                {% endfor %}
            </ul>
            </li>
        {% endfor %}
        </ul>
    
    Note that ``{% regroup %}`` does not order its input! Our example relies on
    the fact that the ``cities`` list was ordered by ``country`` in the first place.
    If the ``cities`` list did *not* order its members by ``country``, the
    regrouping would naively display more than one group for a single country. For
    example, say the ``cities`` list was set to this (note that the countries are not
    grouped together):
    
    .. code-block:: python
    
        cities = [
            {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
            {'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
            {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
            {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
            {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
        ]
    
    With this input for ``cities``, the example ``{% regroup %}`` template code
    above would result in the following output:
    
    * India
    
      * Mumbai: 19,000,000
    
    * USA
    
      * New York: 20,000,000
    
    * India
    
      * Calcutta: 15,000,000
    
    * USA
    
      * Chicago: 7,000,000
    
    * Japan
    
      * Tokyo: 33,000,000
    
    The easiest solution to this gotcha is to make sure in your view code that the
    data is ordered according to how you want to display it.
    
    Another solution is to sort the data in the template using the
    :tfilter:`dictsort` filter, if your data is in a list of dictionaries::
    
        {% regroup cities|dictsort:"country" by country as country_list %}
    
    Grouping on other properties
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Any valid template lookup is a legal grouping attribute for the regroup
    tag, including methods, attributes, dictionary keys and list items. For
    example, if the "country" field is a foreign key to a class with
    an attribute "description," you could use::
    
        {% regroup cities by country.description as country_list %}
    
    Or, if ``country`` is a field with ``choices``, it will have a
    :meth:`~django.db.models.Model.get_FOO_display` method available as an
    attribute, allowing  you to group on the display string rather than the
    ``choices`` key::
    
        {% regroup cities by get_country_display as country_list %}
    
    ``{{ country.grouper }}`` will now display the value fields from the
    ``choices`` set rather than the keys.
    
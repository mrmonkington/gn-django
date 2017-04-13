.. templatetag:: resetcycle

.. function:: resetcycle

    .. versionadded:: 1.11
    
    Resets a previous `cycle`_ so that it restarts from its first item at its next
    encounter. Without arguments, ``{% resetcycle %}`` will reset the last
    ``{% cycle %}`` defined in the template.
    
    Example usage::
    
        {% for coach in coach_list %}
            <h1>{{ coach.name }}</h1>
            {% for athlete in coach.athlete_set.all %}
                <p class="{% cycle 'odd' 'even' %}">{{ athlete.name }}</p>
            {% endfor %}
            {% resetcycle %}
        {% endfor %}
    
    This example would return this HTML::
    
        <h1>José Mourinho</h1>
        <p class="odd">Thibaut Courtois</p>
        <p class="even">John Terry</p>
        <p class="odd">Eden Hazard</p>
    
        <h1>Carlo Ancelotti</h1>
        <p class="odd">Manuel Neuer</p>
        <p class="even">Thomas Müller</p>
    
    Notice how the first block ends with ``class="odd"`` and the new one starts
    with ``class="odd"``. Without the ``{% resetcycle %}`` tag, the second block
    would start with ``class="even"``.
    
    You can also reset named cycle tags::
    
        {% for item in list %}
            <p class="{% cycle 'odd' 'even' as stripe %} {% cycle 'major' 'minor' 'minor' 'minor' 'minor' as tick %}">
                {{ item.data }}
            </p>
            {% ifchanged item.category %}
                <h1>{{ item.category }}</h1>
                {% if not forloop.first %}{% resetcycle tick %}{% endif %}
            {% endifchanged %}
        {% endfor %}
    
    In this example, we have both the alternating odd/even rows and a "major" row
    every fifth row. Only the five-row cycle is reset when a category changes.
    
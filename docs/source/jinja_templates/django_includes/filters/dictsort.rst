.. templatefilter:: dictsort

.. function:: dictsort

    Takes a list of dictionaries and returns that list sorted by the key given in
    the argument.
    
    For example::
    
        {{ value|dictsort:"name" }}
    
    If ``value`` is:
    
    .. code-block:: python
    
        [
            {'name': 'zed', 'age': 19},
            {'name': 'amy', 'age': 22},
            {'name': 'joe', 'age': 31},
        ]
    
    then the output would be:
    
    .. code-block:: python
    
        [
            {'name': 'amy', 'age': 22},
            {'name': 'joe', 'age': 31},
            {'name': 'zed', 'age': 19},
        ]
    
    You can also do more complicated things like::
    
        {% for book in books|dictsort:"author.age" %}
            * {{ book.title }} ({{ book.author.name }})
        {% endfor %}
    
    If ``books`` is:
    
    .. code-block:: python
    
        [
            {'title': '1984', 'author': {'name': 'George', 'age': 45}},
            {'title': 'Timequake', 'author': {'name': 'Kurt', 'age': 75}},
            {'title': 'Alice', 'author': {'name': 'Lewis', 'age': 33}},
        ]
    
    then the output would be::
    
        * Alice (Lewis)
        * 1984 (George)
        * Timequake (Kurt)
    
    ``dictsort`` can also order a list of lists (or any other object implementing
    ``__getitem__()``) by elements at specified index. For example::
    
        {{ value|dictsort:0 }}
    
    If ``value`` is:
    
    .. code-block:: python
    
        [
            ('a', '42'),
            ('c', 'string'),
            ('b', 'foo'),
        ]
    
    then the output would be:
    
    .. code-block:: python
    
        [
            ('a', '42'),
            ('b', 'foo'),
            ('c', 'string'),
        ]
    
    You must pass the index as an integer rather than a string. The following
    produce empty output::
    
        {{ values|dictsort:"0" }}
    
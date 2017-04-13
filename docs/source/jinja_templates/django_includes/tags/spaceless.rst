.. templatetag:: spaceless

.. function:: spaceless

    Removes whitespace between HTML tags. This includes tab
    characters and newlines.
    
    Example usage::
    
        {% spaceless %}
            <p>
                <a href="foo/">Foo</a>
            </p>
        {% endspaceless %}
    
    This example would return this HTML::
    
        <p><a href="foo/">Foo</a></p>
    
    Only space between *tags* is removed -- not space between tags and text. In
    this example, the space around ``Hello`` won't be stripped::
    
        {% spaceless %}
            <strong>
                Hello
            </strong>
        {% endspaceless %}
    
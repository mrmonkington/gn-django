.. templatetag:: verbatim

.. function:: verbatim

    Stops the template engine from rendering the contents of this block tag.
    
    A common use is to allow a JavaScript template layer that collides with
    Django's syntax. For example::
    
        {% verbatim %}
            {{if dying}}Still alive.{{/if}}
        {% endverbatim %}
    
    You can also designate a specific closing tag, allowing the use of
    ``{% endverbatim %}`` as part of the unrendered contents::
    
        {% verbatim myblock %}
            Avoid template rendering via the {% verbatim %}{% endverbatim %} block.
        {% endverbatim myblock %}
    
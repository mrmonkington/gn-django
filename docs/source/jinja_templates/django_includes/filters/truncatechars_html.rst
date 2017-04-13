.. templatefilter:: truncatechars_html

``truncatechars_html``
----------------------

Similar to :tfilter:`truncatechars`, except that it is aware of HTML tags. Any
tags that are opened in the string and not closed before the truncation point
are closed immediately after the truncation.

For example::

    {{ value|truncatechars_html:9 }}

If ``value`` is ``"<p>Joel is a slug</p>"``, the output will be
``"<p>Joel i...</p>"``.

Newlines in the HTML content will be preserved.


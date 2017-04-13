.. templatefilter:: iriencode

``iriencode``
-------------

Converts an IRI (Internationalized Resource Identifier) to a string that is
suitable for including in a URL. This is necessary if you're trying to use
strings containing non-ASCII characters in a URL.

It's safe to use this filter on a string that has already gone through the
:tfilter:`urlencode` filter.

For example::

    {{ value|iriencode }}

If ``value`` is ``"?test=1&me=2"``, the output will be ``"?test=1&amp;me=2"``.


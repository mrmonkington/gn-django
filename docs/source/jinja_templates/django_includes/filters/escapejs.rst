.. templatefilter:: escapejs

``escapejs``
------------

Escapes characters for use in JavaScript strings. This does *not* make the
string safe for use in HTML, but does protect you from syntax errors when using
templates to generate JavaScript/JSON.

For example::

    {{ value|escapejs }}

If ``value`` is ``"testing\r\njavascript \'string" <b>escaping</b>"``,
the output will be ``"testing\\u000D\\u000Ajavascript \\u0027string\\u0022 \\u003Cb\\u003Eescaping\\u003C/b\\u003E"``.


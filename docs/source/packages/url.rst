.. _url-library:

URL
===

General utils
-------------

The following utils can be accessed by importing :code:`gn_django.url.utils`

.. function:: strip_protocol(url)

  Strips the protocol from a URL, converting it to a protocol-relative URL. For instance,
  :code:`https://www.example.com` will be converted to :code:`//www.example.com`.

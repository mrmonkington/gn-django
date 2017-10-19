.. class:: DomainValidator

    The ``DomainValidator`` extends Django's `URLValidator` but will specifically reject
    values that have a protocol. By default, it will also reject values that start with a ``www.``
    subdomain, although this can be disabled by setting the ``allow_www`` parameter to ``True``.

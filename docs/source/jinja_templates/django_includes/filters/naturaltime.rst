.. templatefilter:: naturaltime

.. function:: naturaltime

    For datetime values, returns a string representing how many seconds,
    minutes or hours ago it was -- falling back to the :tfilter:`timesince`
    format if the value is more than a day old. In case the datetime value is in
    the future the return value will automatically use an appropriate phrase.
    
    Examples (when 'now' is 17 Feb 2007 16:30:00):
    
    * ``17 Feb 2007 16:30:00`` becomes ``now``.
    * ``17 Feb 2007 16:29:31`` becomes ``29 seconds ago``.
    * ``17 Feb 2007 16:29:00`` becomes ``a minute ago``.
    * ``17 Feb 2007 16:25:35`` becomes ``4 minutes ago``.
    * ``17 Feb 2007 15:30:29`` becomes ``59 minutes ago``.
    * ``17 Feb 2007 15:30:01`` becomes ``59 minutes ago``.
    * ``17 Feb 2007 15:30:00`` becomes ``an hour ago``.
    * ``17 Feb 2007 13:31:29`` becomes ``2 hours ago``.
    * ``16 Feb 2007 13:31:29`` becomes ``1 day, 2 hours ago``.
    * ``16 Feb 2007 13:30:01`` becomes ``1 day, 2 hours ago``.
    * ``16 Feb 2007 13:30:00`` becomes ``1 day, 3 hours ago``.
    * ``17 Feb 2007 16:30:30`` becomes ``30 seconds from now``.
    * ``17 Feb 2007 16:30:29`` becomes ``29 seconds from now``.
    * ``17 Feb 2007 16:31:00`` becomes ``a minute from now``.
    * ``17 Feb 2007 16:34:35`` becomes ``4 minutes from now``.
    * ``17 Feb 2007 17:30:29`` becomes ``an hour from now``.
    * ``17 Feb 2007 18:31:29`` becomes ``2 hours from now``.
    * ``18 Feb 2007 16:31:29`` becomes ``1 day from now``.
    * ``26 Feb 2007 18:31:29`` becomes ``1 week, 2 days from now``.
    
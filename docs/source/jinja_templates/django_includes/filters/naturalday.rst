.. templatefilter:: naturalday

.. function:: naturalday

    For dates that are the current day or within one day, return "today",
    "tomorrow" or "yesterday", as appropriate. Otherwise, format the date using
    the passed in format string.
    
    **Argument:** Date formatting string as described in the :tfilter:`date` tag.
    
    Examples (when 'today' is 17 Feb 2007):
    
    * ``16 Feb 2007`` becomes ``yesterday``.
    * ``17 Feb 2007`` becomes ``today``.
    * ``18 Feb 2007`` becomes ``tomorrow``.
    * Any other day is formatted according to given argument or the
      :setting:`DATE_FORMAT` setting if no argument is given.
    
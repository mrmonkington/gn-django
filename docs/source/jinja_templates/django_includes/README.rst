README
======

We're collating documentation from Django's docs here, since django-jinja
ports a load of django filters.  To avoid copy/pasting from django's RST docs,
there's a build step.  

Here, we've duplicated django's template reference documentation for: 
 - django general filters (https://raw.githubusercontent.com/django/django/7060f777b09da2a844820a39f227a420c2c6ff90/docs/ref/templates/builtins.txt) 
   in to a file `_django_builtins.rst`.
 - django humanize filters (https://raw.githubusercontent.com/django/django/master/docs/ref/contrib/humanize.txt)
   in to a file `_django_humanize_filters.rst`


Running `extract_jinja_filters.py` will parse django's RST docs, rewrite them
in jinja syntax (and make some formatting changes) and write out 
individual files to `filters/` and `tags/`.  These are then included in our 
one-stop templates documentation in `../using_jinja_templates.rst`.


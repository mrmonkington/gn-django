import sys, os, re, html, csv
from django.utils import timezone
from django.utils.text import slugify
from django.core import exceptions
from django.http import HttpResponse

def is_sphinx_autodoc_running():
    """
    Utility to work out whether the sphinx autodoc module is currently running.

    This can be handy to know since autodoc will attempt to import modules that
    may otherwise assume they are running in a django web app environment.

    Returns True or False
    """
    calling_command = os.path.split(sys.argv[0])[-1]
    return calling_command == 'sphinx-build'

def super_helper():
    return "DW all your problems are now fixed."

def unique_object_slug(obj, source, slug_field='slug', limit=10000):
    """
    Utility for generating unique slugs based on a source string. For instance
    converting an article title of 'Bloodborne 2 Announced' to 'bloodborne-2-announced'.
    If the slug is already taken it will append a numeric value, i.e. 'bloodborne-2-announced-1'
    """
    model = obj.__class__
    base_slug = slugify(source)
    current_slug = base_slug
    search = '%s__startswith' % slug_field
    objects = model.objects.filter(**{search: base_slug})

    for i in range(1, limit):
        o = objects.filter(**{slug_field: current_slug})
        if (len(o) == 0) or (o[0].id == obj.id):
            return current_slug
        current_slug = '%s-%s' % (base_slug, i)

    return False

def htmlify_content(content):
    """
    Replace URLs with links and new lines with ``<br />`` tags, and HTML escape everything else.
    To output in templates, you will need to use the ``safe`` filter.
    """
    url_pattern = re.compile(r'(https?)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
    content = html.escape(content)
    content = re.sub(
        url_pattern,
        lambda c: '<a href="%s" target="_blank">%s</a>' % (c.group(0),c.group(0)),
        content
    )
    return '<br />'.join(content.split('\n'))

def camelize(string):
    """
    Converts snake_case to CamelCase by replacing underscores and spaces with empty
    strings and capitalizing each word. Is not very clever and ignores spaces.
    """
    return ''.join(w.capitalize() for w in re.split(r'[^a-zA-Z0-9]+', string.lower()))

def csv_download_response(column_headings, data, filename, include_date=True):
    """
    Put data into a CSV download response

    Args:
        - ``column_headings``       - A tuple of column headings
        - ``data``                  - An iterable of data. Each value should be tuple of values aligning with
                                    the columns given.
        - ``filename``              - The filename without the `.csv` file extension
        - ``include_date``          - If true, the filename will be appended with a datetime string

    Returns:
        - A tuple containing an ``HttpResponse`` object to be returned by the view, and the
          CSV writer if any more rows needed to be added from outside this function. The
          CSV writer contains the response object so any changes made to the CSV will automatically
          be added to the returned response object.
    """
    if include_date:
        filename = '%s-%s.csv' % (filename, timezone.now().strftime('%Y-%m-%d-%H-%M-%S'))
    else:
        filename = '%s.csv'

    # Build CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response)
    writer.writerow(column_headings)

    for row in data:
        writer.writerow(row)

    return (response, writer)
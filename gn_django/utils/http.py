import csv

from django.http import HttpResponse
from django.utils import timezone


def determine_remote_ip(request):
    """
    Returns the client IP address for the HTTP request.

    This function may return either an IPv4 or an IPv6 address. It may also
    return `None` if an IP cannot be reliably determined (e.g. in a unit test).

    Args:
        * `request` - `HttpRequest`

    Returns:
        `str|None`
    """
    x_client_ip = request.headers.get('X-Client-Ip')
    return x_client_ip if x_client_ip else request.META.get('REMOTE_ADDR')


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
    response = _format_csv_response(filename, include_date)
    writer = csv.writer(response)
    writer.writerow(column_headings)
    for row in data:
        writer.writerow(row)
    return (response, writer)


def csv_download_response_dict(data, filename, include_date=True):
    """
    Same as `csv_download_response` but accepts a list of dicts as data. Does
    not require column headings.

    Note, columns are ordered alphabetically.

    Raises:
        * `ValueError` if data is empty
    """
    if not data:
        raise ValueError('Data is empty')

    # get headings
    headings = sorted(set().union(*(d.keys() for d in data)))

    response = _format_csv_response(filename, include_date)
    writer = csv.DictWriter(response, headings)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    return (response, writer)


def _format_csv_response(filename, include_date):
    if include_date:
        filename = '%s-%s.csv' % (filename, timezone.now().strftime('%Y-%m-%d-%H-%M-%S'))
    else:
        filename = '%s.csv'

    # Build CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

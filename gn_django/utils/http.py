import csv

from django.http import HttpResponse
from django.utils import timezone


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

import re
import urllib.parse as urlparse
from urllib.parse import urlencode

def strip_protocol(url):
    """
    Strip protocol from URL to make it protocol relative
    """
    pattern = re.compile(r'^https?\:')
    return re.sub(pattern, '', url)

def add_params_to_url(url, **params):
    """
    Reliably add a dictionary of GET parameters to a url string.

    Args:
      - `url` - string - the URL string
      - `**params` - kwargs - the GET key/value parameter pairs to add to the URL

    Returns:
      The updated URL string.
    """
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)

def add_path_to_url(url, path):
    """
    Reliably add a path to the end of a url.

    Args:
      - `url` - string - the URL string
      - `path` - string - the path to append to the url

    Returns:
      The updated URL string.
    """
    if url.endswith('/'):
        url = url[:-1]
    if not path.startswith('/'):
        path = '/' + path
    return url + path


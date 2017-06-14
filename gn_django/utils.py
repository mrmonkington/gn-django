import sys, os

import urllib.parse as urlparse
from urllib.parse import urlencode


def is_sphinx_autodoc_running():
    """
    Utility to work out whether the sphinx autodoc module is currently running.

    This can be handy to know since autodoc will attempt to import modules that
    may otherwise assume they are running in a django web app environment.

    Returns True or False
    """
    calling_command = os.path.split(sys.argv[0])[-1]
    return calling_command == 'sphinx-build'

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

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

def convert_camelcase_to_slugified(camelcase):
    """
    Takes a camelcase string and converts it to a string in slug format.

    e.g. 
        "MyStringHere" becomes "my-string-here"

    Args:
      * `camelcase` - string - the camelcase string to convert

    Returns:
      A string.
    """
    slugified = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camelcase)
    slugified = re.sub('([a-z0-9])([A-Z])', r'\1-\2', slugified).lower()
    return slugified

def convert_to_camelcase(to_convert):
    """
    Takes a string and converts it to a string in camelcase format.

    e.g. 
        "my-string-here" becomes "MyStringHere" 
        "my string here" becomes "MyStringHere" 
        "my_string-here" becomes "MyStringHere" 

    Args:
      * `to_convert` - string - the slug string to convert

    Returns:
      A string.
    """
    camelcase = to_convert.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
    return camelcase

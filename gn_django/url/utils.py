import re
import urllib.parse as urlparse
from urllib.parse import urlencode


def strip_protocol(url):
    """
    Strip protocol from URL to make it protocol relative
    """
    pattern = re.compile(r'^https?\:')
    return re.sub(pattern, '', url)


def strip_query_string(url):
    """
    Strip query string from URL
    """
    p = urlparse.urlparse(url)
    return '%s://%s%s' % (p.scheme, p.netloc, p.path)


def add_protocol(url, protocol='http'):
    """
    Checks if a URL has a protocol and adds one if it doesn't.

    Args:
      - `protocol` - string - The protocol to add to the URL, defaults to `http`
    """
    pattern = re.compile(r'^[a-z]+\:\/\/')
    if re.search(pattern, url):
        return url
    url = url.lstrip(':/.')
    return '%s://%s' % (protocol, url)


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


def clean_facebook(string):
    """
    Function for cleaning customer-provided Facebook handle or URL and converting
    into a valid URL
    """
    result = get_handle_from_regex(
        string,
        r'^(?:https?:\/\/)?(?:[Ww]{3}.)?(?:[Ff]acebook\.com\/)?@?((?:profile\.php\?id=)?[a-zA-Z0-9\.\-_]+)'
    )
    if result:
        return 'https://facebook.com/%s' % result


def clean_twitter(string):
    """
    Function for cleaning customer-provided Twitter handle or URL and converting
    into a valid URL
    """
    result = get_handle_from_regex(
        string,
        r'^(?:https?:\/\/)?(?:[Ww]{3}.)?(?:mobile\.)?(?:[Tt]witter\.com\/)?@?([a-zA-Z0-9_]+)'
    )
    if result:
        return 'https://twitter.com/%s' % result


def clean_instagram(string):
    """
    Function for cleaning customer-provided Instagram handle or URL and converting
    into a valid URL
    """
    result = get_handle_from_regex(
        string,
        r'^(?:https?:\/\/)?(?:[Ww]{3}.)?(?:[Ii]nstagram\.com\/)?@?([a-zA-Z0-9_\.]+)'
    )
    if result:
        return 'https://instagram.com/%s' % result


def get_handle_from_regex(string, regex):
    """
    Function for taking a handle from a customer-provided string, i.e. for a social
    media handle. If the string provided is a variation of `NA`, it will return
    `None`. The regular expression must include one capturing group which represents
    the actual handle.
    """
    if string is None:
        return None
    parts = string.split(' ')
    string = parts[0].strip()
    if not string or string.lower() in ['na', 'n/a']:
        return None
    pattern = re.compile(regex)
    result = pattern.search(string)
    if result:
        return result.group(1)


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
    camelcase = re.sub('[^A-Za-z0-9]+', ' ', to_convert).title().replace(' ', '')
    return camelcase

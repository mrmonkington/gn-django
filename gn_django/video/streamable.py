import re


def get_id(url):
    """
    Extract the Streamable ID from a Streamable URL.

    Args:
        * `url` - `string` - The URL to pull the ID from
    Returns:
        * A `string` if successful or `None` if not
    """
    if "streamable" in url:
        match = re.search(r'^https?:\/\/(?:www.)?streamable.com\/(?:[A-Za-z]\/)?([A-Za-z0-9\-_]+)(?:\/)?(?:\?.*)?$', url)
        if match:
            return match.group(1)
    return None

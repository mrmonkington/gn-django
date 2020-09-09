import re


def get_channel(url):
    """
    Extract the Twitch channel name from a Twitch URL.

    Note that the channel name is URL-safe, and may not match the name of the
    Twitch user. You'd need to use the API to check that.

    Args:
        * `url` - `string` - The URL to pull the channel name from
    Returns:
        * A `string` if successful or `None` if not
    """
    if 'twitch' in url:
        match = re.search(
            r'^https?://(?:www\.)?twitch\.tv/([A-Za-z0-9][A-Za-z0-9_]{2,24})/?(?:\?.*)?$',
            url,
        )
        if match:
            return match.group(1)
    return None


def get_vod(url):
    """
    Extract the Twitch VoD ID from a Twitch video URL.

    Video URLs are

    Args:
        * `url` - `string` - The URL to pull the channel name from
    Returns:
        * A `string` if successful or `None` if not
    """
    if 'twitch' in url:
        match = re.search(
            r'^https?://(?:www\.)?twitch\.tv/videos/([0-9]+)/?(?:\?.*)?$',
            url,
        )
        if match:
            return match.group(1)
    return None

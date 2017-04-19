from urllib import parse
import re

def get_id(url):
    """
    Extract the 11 character ID from a YouTube URL. Checks that the URL
    is indeed a YouTube URL, then uses regular expressions to find the ID
    within that URL.
    Args:
        * `url` - `string` - The URL to pull the ID from
    Returns:
        * A `string` if successful or `None` if not
    """
    if "youtu" in url:
        match = re.search(r'^https?:\/\/youtu.be\/([A-Za-z0-9\-_]{11})$', url)
        if match:
            return match.group(1)
        parsed = parse.urlparse(url)
        if parsed.query:
            query = parse.parse_qs(parsed.query)
            key = 'v'
            if key in query:
                vid = query[key][0]
                pattern = re.compile(r'^[A-Za-z0-9\-_]{11}$')
                match = pattern.search(vid)
                if match:
                    return match.group(0)
    return None

def get_thumb(url, type = 'mqdefault'):
    """
    Get the YouTube thumbnail for a valid YouTube URL
    Args:
        * `url` - `string`  - The URL of the video to get the thumbnail for
        * `type` - `string` - The YouTube thumbnail name. Defaults to `mqdefault`
                              as it is a mid quality widescreen image. Options
                              include:
                                  * `default` - Small thumbnail
                                  * `mqdefault` - Medium default (widescreen)
                                  * `maxresdefault` - High res
                                  * `0` - Large thumb
                                  * `1` - Small thumb (first)
                                  * `2` - Small thumb (second)
                                  * `3` - Small thumb (third)
    """
    vid = get_id(url)

    if vid:
        return 'http://i3.ytimg.com/vi/%s/%s.jpg' % (get_id(url), type)
    return None

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from gn_django.video import youtube
import re

class YoutubeValidator(URLValidator):
    """
    Extension of the `URLValidator` class. Validates that a YouTube
    URL is both a valid YouTube URL and contains a valid 11 character ID
    """
    def __call__(self, value):
        """
        Validate the a YouTube URL
        Returns:
            * `string`
        Raises:
            * `ValidatorError`
        """
        super(YoutubeValidator, self).__call__(value)
        if youtube.get_id(value):
            return value
        raise ValidationError('%s is not a valid Youtube URL' % value)

class GamerNetworkImageValidator(URLValidator):
    """
    Extension of the `URLValidator` class. Validates that an image URL links
    to a the Gamer Network CDN
    """
    def __call__(self, value):
        # URL validator will protocol relative URLs, so append protocol and validate that
        with_protocol = re.sub(r'^//', 'http://', value)
        super(GamerNetworkImageValidator, self).__call__(with_protocol)

        patterns = [
            r'^(http)?s?\:?\/\/[a-zA-Z0-9-_]+.gamer\-network.net/',
            r'^(http)?s?\:?\/\/[a-zA-Z0-9-_]+.eurogamer.net/',
        ]

        for p in patterns:
            p = re.compile(p)
            if re.match(p, value):
                return value

        raise ValidationError('%s is not a valid Gamer Network image. Images must be hosted at http://cdn.gamer-network.net' % value)

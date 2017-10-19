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
    
    default_patterns = [
        r'^(http)?s?\:?\/\/[a-zA-Z0-9-_]+.gamer\-network.net/',
        r'^(http)?s?\:?\/\/[a-zA-Z0-9-_]+.eurogamer.net/',
    ]

    def __init__(self, *args, **kwargs):
        super(GamerNetworkImageValidator, self).__init__(*args, **kwargs)
        if kwargs.get('patterns', False):
            self.patterns = kwargs['patterns']
        else:
            self.patterns = self.default_patterns

    def __call__(self, value):
        # URL validator will protocol relative URLs, so append protocol and validate that
        with_protocol = re.sub(r'^//', 'http://', value)
        super(GamerNetworkImageValidator, self).__call__(with_protocol)

        for p in self.patterns:
            p = re.compile(p)
            if re.match(p, value):
                return value

        raise ValidationError('%s is not a valid Gamer Network image. Images must be hosted at http://cdn.gamer-network.net' % value)

class DomainValidator(URLValidator):
    patterns = [
        r'^([a-z]+)?\:?\/\/',
        r'^www\.?'
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_www = kwargs.get('allow_www', False)
    
    def __call__(self, value):
        for pattern in self.patterns:
            if re.search(pattern, value):
                raise ValidationError('Domain should not contain protocol (e.g. \'http://\') or \'www.\' subdomain')
        try:
            super().__call__('http://%s' % value)
        except ValidationError:
            raise ValidationError('\'%s\'is not a valid domain' % value)

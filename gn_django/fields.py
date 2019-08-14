from django.db import models
from django.utils import timezone
from pytz import common_timezones

from .validators import YoutubeValidator


class TimezoneField(models.CharField):
    """
    A field for selecting a timezone from the common timezones list.
    """
    def __init__(self, *args, **kwargs):
        common_timezone_names = [tz.replace('_', ' ') for tz in common_timezones]
        the_kwargs = {
            'choices': zip(common_timezones, common_timezone_names),
            'default': timezone.get_default_timezone_name(),
            'max_length': 50,
        }
        the_kwargs.update(kwargs)
        super().__init__(*args, **the_kwargs)


class YoutubeField(models.CharField):
    """
    Field representing a YouTube video, essentially just a text field
    but with automatic validation that given values are valid YouTube URLs
    """

    default_validators = [YoutubeValidator()]

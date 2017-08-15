from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from .validators import YoutubeValidator

class YoutubeField(models.CharField):
    """
    Field representing a YouTube video, essentially just a text field
    but with automatic validation that given values are valid YouTube URLs
    """

    default_validators = [YoutubeValidator()]

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


class UniqueBooleanField(BooleanField):
    """
    Like a ``BooleanField`` except there can be only one row in the table with
    a value of ``True``.
    """
    def pre_save(self, model_instance, add):
        objects = model_instance.__class__.objects
        if objects.filter(**{self.attname: True}).exists():
            raise ValueError(f'{self.name} cannot be `True` for more than '
                             f'one {self.model.__name__}')
        return getattr(model_instance, self.attname)


from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from gn_django.form.autocomplete import AutocompleteSelectField as AutocompleteSelectFormField
from .validators import YoutubeValidator

class YoutubeField(models.CharField):
    """
    Field representing a YouTube video, essentially just a text field
    but with automatic validation that given values are valid YouTube URLs
    """

    default_validators = [YoutubeValidator()]

class AutocompleteSelectField(models.Field):
    def __init__(self, *args, **kwargs):
        self.form_defaults = {
            'form_class': AutocompleteSelectFormField
        }

        for k in AutocompleteSelectFormField.ac_kwargs:
            if kwargs.get(k, False):
                self.form_defaults[k] = kwargs[k]
                del kwargs[k]
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        self.form_defaults.update(kwargs)
        return super().formfield(**self.form_defaults)

from django.db import models
from gn_django import fields, validators

class FieldValidatorExample(models.Model):
    youtube = fields.YoutubeField(max_length=255, blank=True, null=True, help_text="The <code>YoutubeField</code> includes the <code>YoutubeValidator</code> by default.")
    youtube_validator = models.CharField(max_length=255, blank=True, null=True, validators=[validators.YoutubeValidator()], help_text="This is a regular old <code>CharField</code>, but has the <code>YoutubeValidator</code> assigned to it.")
    gn_image_validator = models.CharField(max_length=255, blank=True, null=True, validators=[validators.GamerNetworkImageValidator()], help_text="This is a regular old <code>CharField</code>, but still has the <code>GamerNetworkImageValidator()</code> assigned to it, and so only accepts images from Gamer Network's CDN.")

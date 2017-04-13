from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify

import jinja2
from django_jinja.backend import Jinja2 as DjangoJinja2

from .extensions import SpacelessExtension
from .globals import random

def environment(**options):
    """
    Magnet base jinja2 environment.
    """
    if options.get('extensions'):
        options['extensions'].append(SpacelessExtension)
    env = jinja2.Environment(**options)
    return env

class Jinja2(DjangoJinja2):
    
    def __init__(self, params):
        params = params.copy()
        options = params.get("OPTIONS", {})
        if not options.get('environment'):
            options['environment'] = "gn_django.template.backend.environment"
        super(Jinja2, self).__init__(params)


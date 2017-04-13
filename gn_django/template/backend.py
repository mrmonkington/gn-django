from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify

import jinja2
from django_jinja.backend import Jinja2 as DjangoJinja2
from django_jinja import builtins as dj_jinja_builtins

from .extensions import SpacelessExtension
from .globals import random

def environment(**options):
    """
    Base jinja2 environment.
    """
    env = jinja2.Environment(**options)
    return env

class Jinja2(DjangoJinja2):
    
    def __init__(self, params):
        params = params.copy()
        options = params.get("OPTIONS", {})
        options['environment'] = options.pop('environment', "gn_django.template.backend.environment")
        base_extensions = self.get_base_extensions()
        options['extensions'] = base_extensions + options.pop('extensions', [])
        super(Jinja2, self).__init__(params)

    def get_base_extensions(self):
        base_extensions = dj_jinja_builtins.DEFAULT_EXTENSIONS
        # NOTE: Add more custom extensions here
        base_extensions.append(SpacelessExtension)
        return base_extensions


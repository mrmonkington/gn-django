from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify

import jinja2
from django_jinja.backend import Jinja2 as DjangoJinja2
from django_jinja import builtins as dj_jinja_builtins
from django_jinja.contrib._humanize.templatetags._humanize import ordinal, intcomma, intword, apnumber, naturalday, naturaltime

from .extensions import SpacelessExtension
from .globals import random

def environment(**options):
    """
    Base jinja2 environment.
    """
    env = jinja2.Environment(**options)
    return env

class Jinja2(DjangoJinja2):
    """
    An overridable Jinja2 backend.

    This offers hooks to override the default set of filters, globals, tests
    and extensions available in the Jinja2 templating environment.
    """
    
    def __init__(self, params):
        params = params.copy()
        options = params.get("OPTIONS", {})
        options['environment'] = options.pop('environment', "gn_django.template.backend.environment")
        base_extensions = self.get_base_extensions()
        options['extensions'] = base_extensions + options.pop('extensions', [])
        base_filters = self.get_base_filters()
        base_filters.update(options.pop('filters', {}))
        options['filters'] = base_filters
        base_tests = self.get_base_tests()
        base_tests.update(options.pop('tests', {}))
        options['tests'] = base_tests
        base_globals = self.get_base_globals()
        base_globals.update(options.pop('globals', {}))
        options['globals'] = base_globals
        params['OPTIONS'] = options
        super(Jinja2, self).__init__(params)

    def get_base_filters(self):
        """
        Default filters that should be included for all jinja templates
        rendered from gn-django.

        Returns:
            iterable of filters
        """
        base_filters = {
            'ordinal': ordinal,
            'intcomma': intcomma,
            'intword': intword,
            'apnumber': apnumber,
            'naturalday': naturalday,
            'naturaltime': naturaltime,
        }
        return base_filters

    def get_base_globals(self):
        """
        Default globals that should be included for all jinja templates
        rendered from gn-django.

        Returns:
            iterable of globals
        """
        base_globals = {}
        return base_globals

    def get_base_tests(self):
        """
        Default tests that should be included for all jinja templates
        rendered from gn-django.

        Returns:
            iterable of tests
        """
        base_tests = {}
        return base_tests

    def get_base_extensions(self):
        """
        Default extensions that should be included for all jinja templates
        rendered from gn-django.

        Returns:
            iterable of extensions
        """
        base_extensions = dj_jinja_builtins.DEFAULT_EXTENSIONS
        base_extensions.append(SpacelessExtension)
        return base_extensions


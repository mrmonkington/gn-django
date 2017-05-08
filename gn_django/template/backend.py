from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify

import jinja2
from django_jinja.backend import Jinja2 as DjangoJinja2
from django_jinja import builtins as dj_jinja_builtins
from django_jinja.contrib._humanize.templatetags._humanize import ordinal, intcomma, intword, apnumber, naturalday, naturaltime

from .extensions import SpacelessExtension
from .globals import randint

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

    Constructor args:
      * ``params`` - dictionary with possible key/value pairs:
        * ``"OPTIONS"`` - dictionary with possible key/value pairs:
          * ``"app_dirname"`` - the directory name that jinja templates are stored in
            per application.
          * ``"context_processors"`` - list of context processors which will be
            called to add some global context to all jinja template rendering.
            Should be a list of dot-notation string python callables
            e.g. ``["gn_django.template.context_processors.settings"]``
          * ``"match_extension"`` - selectively use this jinja backend when the
            template name has an extension that matches this setting.  e.g.:
            ``".jinja"``
            This should be set to ``None`` if this backend should be tried for
            rendering any template.  Note that Django will go through all backends specified
            in order of the ``TEMPLATES`` setting until one yields a rendered template
            or all backends have been tried.  So the ``"match_extension"`` option
            should be unnecessary unless a single app uses a mix of django and
            jinja templating - which is crazy and not recommended.
          * ``"match_regex"`` - selectively use this jinja backend when the
            template name matches this regex.  e.g.:
            ``".*\.jinja"``
          * ``"environment"`` - python dot-notation string for the jinja
            environment callable.
          * ``"filters"`` - dictionary of extra jinja filters to include in the
            template environment.  The dictionary should have keys as filter name
            and values as filter callable (or a string dot-notation python path
            of the callable)
          * ``"tests"`` - dictionary of extra jinja tests to include in the
            template environment.  The dictionary should have keys as test name
            and values as test callable (or a string dot-notation python path
            of the
          * ``"globals"`` - dictionary of extra jinja globals to include in the
            template environment.  The dictionary should have keys as global name
            and values as global callable (or a string dot-notation python path
            of the
          * ``"constants"`` - dictionary of extra jinja constants to include in the
            template environment.  The dictionary should have keys as constant name
            and values as constant value.
          * ``"loader"`` - the template loader to use for loading jinja templates.
            This defaults to a standard filesystem loader, but can be specified
            as either a dot-notation python path or a fully instantiated loader
            object
    """

    def __init__(self, params):
        """
        """
        params = params.copy()
        options = params.get("OPTIONS", {})
        options['environment'] = options.pop('environment', "gn_django.template.backend.environment")

        # To define additional base extensions, extend `get_base_extensions()` method
        base_extensions = self.get_base_extensions()
        options['extensions'] = base_extensions + options.pop('extensions', [])

        # To define additional base filters, extend `get_base_filters()` method
        base_filters = self.get_base_filters()
        base_filters.update(options.pop('filters', {}))
        options['filters'] = base_filters

        # To define additional base tests, extend `get_base_tests()` method
        base_tests = self.get_base_tests()
        base_tests.update(options.pop('tests', {}))
        options['tests'] = base_tests

        # To define additional base globals, extend `get_base_globals()` method
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
        base_globals = {
            'randint': randint,
        }
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
        base_extensions = dj_jinja_builtins.DEFAULT_EXTENSIONS.copy()
        base_extensions.append(SpacelessExtension)
        return base_extensions

import weakref

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify
from django.utils import six
from django.utils.module_loading import import_string

import jinja2
from django_jinja.backend import Jinja2 as DjangoJinja2
from django_jinja import builtins as dj_jinja_builtins
from django_jinja.contrib._humanize.templatetags._humanize import ordinal, intcomma, intword, apnumber, naturalday, naturaltime

from .extensions import SpacelessExtension, IncludeWithExtension
from .globals import random

class Environment(jinja2.Environment):
    """
    Custom Jinja Environment class for gn django projects.

    This provides an override for generating template cache keys - the cache
    is used in preference to the template loader.  By default, keys are a 
    combination of loader reference and template name.

    Extra kwargs:
      * `template_cache_key_cb` - a callback function for generating a template
        cache key.  When this is present, this is used instead of the default
        cache key behaviour.

    *NOTE*: This class has some duplication from jinja2.Environment which is
    currently unavoidable as there's no overridable hook just for generating
    template cache keys: https://github.com/pallets/jinja/blob/bbe0a4174c2846487bef4328b309fddd8638da39/jinja2/environment.py#L798
    """

    def __init__(self, **kwargs):
        self.template_cache_key_cb = kwargs.pop('template_cache_key_cb', None)
        super(Environment, self).__init__(**kwargs)

    def get_template_cache_key(self, template_name):
        """
        Generates a cache key for the given template name.

        This will use `template_cache_key_cb` if it is present on the object
        instance.
        """
        cache_key = (weakref.ref(self.loader), template_name)
        if self.template_cache_key_cb:
            if isinstance(self.template_cache_key_cb, six.string_types):
                self.template_cache_key_cb = import_string(self.template_cache_key_cb)
            cache_key = self.template_cache_key_cb(self.loader, template_name)
        return cache_key

    @jinja2.utils.internalcode
    def _load_template(self, name, globals):
        if self.loader is None:
            raise TypeError('no loader for this environment specified')
        # TODO: Maybe see if we can merge a PR in to the jinja project which
        # provides `get_template_cache_key` for override
        cache_key = self.get_template_cache_key(name)
        if self.cache is not None:
            template = self.cache.get(cache_key)
            if template is not None and (not self.auto_reload or
                                         template.is_up_to_date):
                return template
        template = self.loader.load(self, name, globals)
        if self.cache is not None:
            self.cache[cache_key] = template
        return template

def environment(**options):
    """
    Base jinja2 environment.
    """
    env = Environment(**options)
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
        base_extensions = dj_jinja_builtins.DEFAULT_EXTENSIONS.copy()
        base_extensions.append(SpacelessExtension)
        base_extensions.append(IncludeWithExtension)
        return base_extensions

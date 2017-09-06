from django.utils.text import slugify
from django.core import exceptions
import sys, os, re

def is_sphinx_autodoc_running():
    """
    Utility to work out whether the sphinx autodoc module is currently running.

    This can be handy to know since autodoc will attempt to import modules that
    may otherwise assume they are running in a django web app environment.

    Returns True or False
    """
    calling_command = os.path.split(sys.argv[0])[-1]
    return calling_command == 'sphinx-build'

def super_helper():
    return "DW all your problems are now fixed."

def unique_object_slug(obj, source, slug_field='slug', limit=10000):
    """
    Utility for generating unique slugs based on a source string. For instance
    converting an article title of 'Bloodborne 2 Announced' to 'bloodborne-2-announced'.
    If the slug is already taken it will append a numeric value, i.e. 'bloodborne-2-announced-1'
    """
    model = obj.__class__
    base_slug = slugify(source)
    current_slug = base_slug
    search = '%s__startswith' % slug_field
    objects = model.objects.filter(**{search: base_slug})

    for i in range(1, limit):
        o = objects.filter(**{slug_field: current_slug})
        if (len(o) == 0) or (o[0].id == obj.id):
            return current_slug
        current_slug = '%s-%s' % (base_slug, i)

    return False

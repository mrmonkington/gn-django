import os
import sys

from django.db.models import QuerySet


def super_helper():
    return "DW all your problems are now fixed."


def all_subclasses(cls):
    """
    Gets all subclasses of a class.
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def count(countable):
    """
    Return the number of items in a QuerySet or other container.

    If given a QuerySet object, this will use the count() method. Otherwise, it
    falls back to using len().

    This method offers a little convenience when duck-typing something that may
    either be a QuerySet or a plain iterable, allowing you to pick the most
    efficient method of counting available for the presented object.

    However, note that it is NOT always more efficient to use count() over
    len() with QuerySet objects. See the Django docs for a discussion on this:
      https://docs.djangoproject.com/en/3.1/ref/models/querysets/#count
    """
    if isinstance(countable, QuerySet):
        return countable.count()
    else:
        return len(countable)


def is_sphinx_autodoc_running():
    """
    Utility to work out whether the sphinx autodoc module is currently running.

    This can be handy to know since autodoc will attempt to import modules that
    may otherwise assume they are running in a django web app environment.

    Returns True or False
    """
    calling_command = os.path.split(sys.argv[0])[-1]
    return calling_command == 'sphinx-build'

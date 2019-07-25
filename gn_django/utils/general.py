import os
import sys


def super_helper():
    return "DW all your problems are now fixed."


def all_subclasses(cls):
    """
    Gets all subclasses of a class.
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def is_sphinx_autodoc_running():
    """
    Utility to work out whether the sphinx autodoc module is currently running.

    This can be handy to know since autodoc will attempt to import modules that
    may otherwise assume they are running in a django web app environment.

    Returns True or False
    """
    calling_command = os.path.split(sys.argv[0])[-1]
    return calling_command == 'sphinx-build'

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

def convert_camelcase_to_slugified(camelcase):
    """
    Takes a camelcase string and converts it to a string in slug format.

    e.g. 
        "MyStringHere" becomes "my-string-here"

    Args:
      * `camelcase` - string - the camelcase string to convert

    Returns:
      A string.
    """
    slugified = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camelcase)
    slugified = re.sub('([a-z0-9])([A-Z])', r'\1-\2', slugified).lower()
    return slugified

def super_helper():
    return "DW all your problems are now fixed."

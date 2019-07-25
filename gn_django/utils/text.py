import re


def camelize(string):
    """
    Converts snake_case to CamelCase by replacing underscores and spaces with empty
    strings and capitalizing each word. Is not very clever and ignores spaces.
    """
    return ''.join(w.capitalize() for w in re.split(r'[^a-zA-Z0-9]+', string.lower()))

import re


def camelize(string):
    """
    Converts snake_case to CamelCase by replacing underscores and spaces with empty
    strings and capitalizing each word. Is not very clever and ignores spaces.
    """
    return ''.join(w.capitalize() for w in re.split(r'[^a-zA-Z0-9]+', string.lower()))


def remove_emojis(string):
    """
    Remove emojis and other ideograms from strings.
    Stolen from https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
    """
    pattern = re.compile(pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags = re.UNICODE)
    return pattern.sub(r'',string)
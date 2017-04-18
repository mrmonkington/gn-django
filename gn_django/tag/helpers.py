def tag_comma_split(string):
    """
    Split tags at commas
    """
    return [t.strip() for t in string.split(',') if t]

def tag_comma_join(tags):
    """
    Join tags with commas
    """
    return ', '.join(t.name for t in tags)

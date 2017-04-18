def super_helper():
    return "DW all your problems are now fixed."

def strip_protocol(url):
    """
    Strip protocol from URL to make it protocol relative
    """
    pattern = re.compile(r'^https?\:')
    return re.sub(pattern, '', url)

from random import randint

def random(limit):
    """
    Generate a random integer between 1 and `limit`
    Args:
        * `limit` - `integer` - The max number that can be generated
    Returns:
        A random integer
    Usage:
        ``random(100)``
    """
    return randint(1, limit)

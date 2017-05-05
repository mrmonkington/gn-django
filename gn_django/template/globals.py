from random import randint

def random(maximum=100, minimum=0):
    """
    Generate a random integer between `minimum` and `maximum`.
    Args:
        - `maximum` - The maximum integer that can be generated (defaults to 100)
        - `minimum` - The minimum integer that can be generated (defaults to 0)
    Returns:
        A random integer
    Usage:
        ``random()``
        ``random(300)``
        ``random(10, 5)``
        ``random(minimim=20, maximum=40)``
    """
    return randint(minimum, maximum)

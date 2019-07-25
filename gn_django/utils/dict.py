from itertools import zip_longest


def compare_dicts(dict_1, dict_2):
    """
    Compare two dictionaries and return a fresh dictionary indicating the differences
    between the two of them.

    For each item in the dictionaries, True indicates a value has changed,
    False indicates that the two values are identical.

    Args:
         `dict_1` - `dict`
         `dict_2` - `dict`

    Returns:
        `dict` - A dict whose structure will mirror that of the provided arguments,
        and whose leaf values will always be boolean, with True indicating that the
        field differs between the two objects, and False indicating they're the same.
    """
    def _diff_values(value_1, value_2):
        """
        Compare two values and return True if they're different, False if they're
        the same. If the values are structures, runs comparison recursively inside
        those structures so each item will be True/False (or another strucutre).

        Args:
             `value_1` - mixed
             `value_2` - mixed

        Returns:
            `bool` or `dict` or `list`
        """
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            return compare_dicts(value_1, value_2)
        elif isinstance(value_1, (list, set, tuple)) and isinstance(value_2, (list, set, tuple)):
            return [
                _diff_values(inner_1, inner_2)
                for inner_1, inner_2 in zip_longest(value_1, value_2)
            ]

        return value_1 != value_2

    diff = {}

    for key in set(dict_1) | set(dict_2):
        try:
            diff[key] = _diff_values(dict_1[key], dict_2[key])
        except KeyError:
            diff[key] = True

    return diff


def flatten_dict(data, prefix=''):
    """
    Flatten the given dictionary, returning a one-dimensional dictionary whose
    keys use the naming pattern for nested model fields.

    e.g. if you have a dict with {'foo': {'bar': {'baz': 123}}}, the return
    value will contain {'foo__bar__baz': 123}.

    Args:
        `data` - `dict` - Dictionary to be flattened.
        `prefix` - `str` - Apply a string prefix to all key names.

    Returns:
        `dict`
    """
    flattened = {}

    for key, value in data.items():
        if isinstance(value, (dict, list, set, tuple)):
            flattened.update(flatten_dict(
                data=value if isinstance(value, dict) else dict(enumerate(value)),
                prefix=(prefix + key + '__') if prefix is not None else None
            ))
        else:
            flattened['%s%s' % (prefix if prefix is not None else '', key)] = value

    return flattened

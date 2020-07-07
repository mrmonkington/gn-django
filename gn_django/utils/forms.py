def qs_to_choices(qs, val_field, label_field):
    """
    Convert a queryset of objects into a tuple of choices suitable for a choice
    field.

    Args:
        * `qs` - `QuerySet`
        * `val_field` - `string` - attribute of object to be used as choice
        value, e.g. 'id', 'slug', etc.
        * `label_field` - `string` - attribute of object to be used as label,
        e.g. 'name', etc.
    """
    return tuple(
        (
            getattr(instance, val_field),
            getattr(instance, label_field)
        ) for instance in qs
    )

def qs_to_choices(qs, val_field=None, label_field=None):
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
    choices = []
    for instance in qs:
        value = getattr(instance, val_field) if val_field else instance.pk
        label = getattr(instance, label_field) if label_field else str(instance)
        choices.append([value, label])
    return choices

def forms_valid(forms):
    """
    Validate multiple forms.

    Args:
        `forms` - `iterable` - a collection of form objects.

    Returns:
        `bool` - True if all forms passed in are valid.
    """
    valid = True
    for f in forms:
        if f:
            valid = bool(valid and f.is_valid())
    return valid

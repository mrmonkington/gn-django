from django.forms.models import ModelChoiceField


class LazyModelChoiceField(ModelChoiceField):
    """
    For use with widgets that pull choices using AJAX.

    `ModelChoiceField` iterates over the entire queryset on page load. In some
    cases this can be quite expensive. By settings `choices` to an empty list
    we avoid this unnecessary querying.
    """
    choices = []

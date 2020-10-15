from functools import partial
from itertools import groupby
from operator import attrgetter

from django.forms.models import (
    ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField
)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ('', self.field.empty_label)
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in groupby(queryset, self.groupby):
            yield (group, [self.choice(obj) for obj in objs])


class BaseGroupedModelChoiceField:

    def __init__(self, *args, group_by_field, **kwargs):
        if isinstance(group_by_field, str):
            group_by_field = attrgetter(group_by_field)
        elif not callable(group_by_field):
            raise TypeError(
                'group_by_field must either be a str or a callable accepting '
                'a single argument'
            )
        self.iterator = partial(
            GroupedModelChoiceIterator,
            groupby=group_by_field
        )
        super().__init__(*args, **kwargs)


class GroupedModelChoiceField(BaseGroupedModelChoiceField, ModelChoiceField):
    pass


class GroupedModelMultiChoiceField(BaseGroupedModelChoiceField, ModelMultipleChoiceField):
    pass

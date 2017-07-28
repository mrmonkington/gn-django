from dal_select2.views import autocomplete as base_autocomplete

class AutocompleteView(base_autocomplete.Select2QuerySetView):
    def __init__(self, model, field, *args, **kwargs):
        self.model = model
        self.field = field
        super(AutocompleteView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        self.validate_usage()
        models = self.model.all()
        if self.q:
            kwargs = {'%s__istartswith' % self.field: self.q}
            models = models.filter(**kwargs)

        return models

    def validate_usage(self):
        return

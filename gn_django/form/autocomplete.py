from dal_select2.views import Select2QuerySetView

class AutocompleteView(Select2QuerySetView):
    def get_option_list(self):
        raise NotImplementedError('Must declare `get_option_list()` method on class that extends `gn_django.form.autocomplete.AutocompleteView`')

    def get_context_data(self, *args, **kwargs):
        return super(AutocompleteView, self).get_context_data(object_list=self.get_option_list(), *args, **kwargs)

    def get_queryset(self):
        """
        Bypass `get_queryset()`. The `django-autocomplete-light` extension assumes
        that the autocomplete field will be used in conjunction with the Django ORM.
        Instead, logic to load autocomplete suggestions should be in `get_option_list()`
        """
        return

    def get_result_value(self, result):
        if isinstance(result, dict):
            return result.get('value', result['label'])
        return result

    def get_result_label(self, result):
        if isinstance(result, dict):
            return result['label']
        return result

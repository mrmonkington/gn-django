import re
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .exceptions import ImproperlyConfigured

class SearchableQuerySetMixin:
    ignored_words = ['the', 'and']
    min_length = 3

    @property
    def search_fields(self):
        raise ImproperlyConfigured('`search_fields` attribute must be set')

    def search(self, search_term, term_limit=5):
        qs = self.all()
        count = 0
        terms = self._get_search_terms(search_term)
        for term in terms:
            term = term.strip('"')
            if count >= term_limit:
                raise ValidationError(_('Too many search terms, please use no more than %s. Note: Common words, repeated words, and words shorter than three characters are automatically removed and not counted.' % term_limit))
            fields = self.search_fields
            q = None
            for field in self.search_fields:
                field_q = Q(**{'%s__icontains' % field: term})
                if q is None:
                    q = field_q
                else:
                    q = q|field_q
            matches = self.filter(q)
            qs = qs & matches
            count += 1
        return qs.distinct()

    def _get_search_terms(self, search_term):
        phrase_pattern = re.compile(r'\"[^\"]+\"')
        phrases = re.findall(phrase_pattern, search_term)
        for phrase in phrases:
            search_term = search_term.replace(phrase, '')
        terms = search_term.split(' ')
        terms = [t for t in terms if len(t) >= self.min_length and t not in self.ignored_words]
        terms = set(phrases + terms)
        return terms

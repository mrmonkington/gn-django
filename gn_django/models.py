import re
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .exceptions import ImproperlyConfigured

class SearchableQuerySetMixin:
    """
    Mixin for query sets to extend. This adds some configurable search functionality
    to query sets.
    """
    ignored_words = ['the', 'and']
    min_length = 3

    @property
    def search_fields(self):
        """
        A list of fields to check when running a search. This should not include
        the ``icontains`` modifier as this will be automatically appended. It can,
        however, check foreign key fields in the same way you would in a regular filter,
        i.e. ``user__email``. The fields will be checked separately with an OR, so
        if you have ``['email','name']``, it will return any models that match in
        either the ``email`` or the ``name`` fields.
        """
        raise ImproperlyConfigured('`search_fields` attribute must be set')

    def search(self, search_term, term_limit=5):
        """
        Conduct a search on all fields declared in ``self.search_fields`` using any words
        or quote-encased phrases declared in the ``search_term`` string. Any words shorter
        than ``self.min_length`` or declared in ``self.ignored_words`` will be ignored.
        If the number of unique words/phrases is greater than ``term_limit``, an exception
        will be thrown.
        """
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
        """
        Split out individual words and quote-encased phrases into a set
        of unique search terms.
        """
        phrase_pattern = re.compile(r'\"[^\"]+\"')
        phrases = re.findall(phrase_pattern, search_term)
        for phrase in phrases:
            search_term = search_term.replace(phrase, '')
        terms = search_term.split(' ')
        terms = [t for t in terms if len(t) >= self.min_length and t not in self.ignored_words]
        terms = set(phrases + terms)
        return terms

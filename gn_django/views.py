from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic.detail import SingleObjectMixin


class HashedObjectMixin(SingleObjectMixin):
    """
    Provide the ability to retrieve a single object with a hash ID.
    """
    hashid_url_kwarg = 'hash'

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Requires `self.queryset` and a `hash` argument in the URLconf.
        """
        hashid = self.kwargs.get(self.hashid_url_kwarg)

        if hashid is None:
            raise AttributeError(
                'Generic detail view %s must be called with a hashid in the '
                'URLconf.' % self.__class__.__name__
            )

        try:
            obj = self.model._default_manager.get_by_hashid(hashid)
        except self.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query") %
                {'verbose_name': self.model._meta.verbose_name}
            )
        return obj


class NoIndexMixin:
    """
    Adds a noindex header to a template response.
    """
    def render_to_response(self, context, **response_kwargs):
        resp = super().render_to_response(context, **response_kwargs)
        resp.setdefault('X-Robots-Tag', 'noindex')
        return resp

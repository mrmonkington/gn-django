from django.views.generic import TemplateView

from gn_django.site_domain import get_current_site_domain, get_namespace_for_site_domain

class DomainView(TemplateView):

    template_name = "domain.html"

    def get_context_data(self):
        return {
            'domain': get_current_site_domain(),
            'namespace': get_namespace_for_site_domain(),
        }

    

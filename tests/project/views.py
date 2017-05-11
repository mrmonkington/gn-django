from django.views.generic import TemplateView

from gn_django.site import get_current_site, get_namespace_for_site

class DomainView(TemplateView):

    template_name = "site.j2"

    def get_context_data(self):
        return {
            'site': get_current_site(),
            'namespace': get_namespace_for_site(),
        }

    

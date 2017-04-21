from django.conf import settings

from .site_domains import get_current_site_domain, set_current_site_domain, clear_current_site_domain

class SiteDomainMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        host = request.get_host().split(':')[0]
        site_domain = host
        try:
            site_domain = settings.SITE_DOMAIN_MAPPER[host]
        except KeyError:
            raise Exception("settings file's SITE_DOMAIN_MAPPER attribute does not have an entry for the host %s" % host)
        set_current_site_domain(site_domain)

        response = self.get_response(request)

        clear_current_site_domain()

        return response

    def process_exception(self, request, exception):
        clear_current_site_domain()
        return None

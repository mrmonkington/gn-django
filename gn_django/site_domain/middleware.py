from django.conf import settings

from .site_domains import get_current_site_domain, set_current_site_domain, clear_current_site_domain

class SiteDomainMiddleware:
    """
    Middleware identifies the Host set for incoming requests and uses
    `set_current_site_domain()` to set thread local storage of the current
    site domain.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # Identify the Host and lookup the site domain from SITE_DOMAIN_MAPPER
        # in django settings
        host = request.get_host().split(':')[0]
        site_domain = host
        try:
            site_domain = settings.SITE_DOMAIN_MAPPER[host]
        except KeyError:
            raise KeyError("django setting's SITE_DOMAIN_MAPPER attribute does not have an entry for the host '%s'" % host)
        # Set the thread local storage
        set_current_site_domain(site_domain)

        response = self.get_response(request)

        # Clear the thread local storage
        clear_current_site_domain()

        return response

    def process_exception(self, request, exception):
        # Ensure that we clear the TLS for requests that raise an exception
        clear_current_site_domain()
        return None

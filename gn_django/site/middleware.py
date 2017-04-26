from django.conf import settings

from .site import get_current_site, set_current_site, clear_current_site

class SiteFromDomainMiddleware:
    """
    Middleware identifies the Host set for incoming requests and uses
    `set_current_site()` to set thread local storage of the current
    site.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # Identify the Host and lookup the site domain from SITE_DOMAINS
        # in django settings
        host = request.get_host().split(':')[0]
        site = host
        try:
            site = settings.SITE_DOMAINS[host]
        except KeyError:
            raise KeyError("django setting's SITE_DOMAINS attribute does not have an entry for the host '%s'" % host)
        # Set the thread local storage
        set_current_site(site)

        response = self.get_response(request)

        # Clear the thread local storage
        clear_current_site()

        return response

    def process_exception(self, request, exception):
        # Ensure that we clear the TLS for requests that raise an exception
        clear_current_site()
        return None

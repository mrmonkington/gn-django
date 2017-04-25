from threading import local

from django.conf import settings

_active = local()

def get_current_site_domain():
    """
    Get the site domain for the current thread.
    """
    site_domain = getattr(_active, "current_site_domain", None)
    return site_domain

def set_current_site_domain(site_domain):
    """
    Set the site domain for the current thread.
    """
    _active.current_site_domain = site_domain

def clear_current_site_domain():
    """
    Clear the site domain in the current thread, if it was set.
    """
    if hasattr(_active, "current_site_domain"):
        del _active.current_site_domain

def get_namespace_for_site_domain():
    """
    Get the namespace string for the currently active site
    domain.
    """
    if not hasattr(settings, "SITE_DOMAIN_NAMESPACE_MAPPER"):
        raise Exception("get_namespace_for_site_domain function can only be called if SITE_DOMAIN_NAMESPACE_MAPPER is defined in the settings.")

    site_domain = get_current_site_domain()
    if site_domain == None:
        return None
    try:
        return settings.SITE_DOMAIN_NAMESPACE_MAPPER[site_domain]
    except KeyError:
        raise KeyError("SITE_DOMAIN_NAMESPACE_MAPPER setting has no key '%s'" % site_domain)

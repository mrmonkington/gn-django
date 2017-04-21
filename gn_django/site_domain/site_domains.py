from threading import local

from django.conf import settings

_active = local()

def get_current_site_domain():
    """
    Get the domain for the current request
    """
    site_domain = getattr(_active, "current_site_domain", None)
    return site_domain

def set_current_site_domain(site_domain):
    """
    Set the current domain.
    """
    _active.current_site_domain = site_domain

def clear_current_site_domain():
    """
    Deactivate the property that was set
    """
    if hasattr(_active, "current_site_domain"):
        del _active.current_site_domain

def get_namespace_for_site_domain():
    if not hasattr(settings, "SITE_DOMAIN_NAMESPACE_MAPPER"):
        raise Exception("get_namespace_for_site_domain function can only be called \
            SITE_DOMAIN_NAMESPACE_MAPPER is defined in the settings.")

    site_domain = get_current_site_domain()
    return settings.SITE_DOMAIN_NAMESPACE_MAPPER[site_domain]

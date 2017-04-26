from threading import local

from django.conf import settings

_active = local()

def get_current_site():
    """
    Get the site domain for the current thread.
    """
    site = getattr(_active, "current_site", None)
    return site

def set_current_site(site):
    """
    Set the site domain for the current thread.
    """
    _active.current_site = site

def clear_current_site():
    """
    Clear the site domain in the current thread, if it was set.
    """
    if hasattr(_active, "current_site"):
        del _active.current_site

def get_namespace_for_site():
    """
    Get the namespace string for the currently active site
    domain.
    """
    if not hasattr(settings, "SITE_NAMESPACES"):
        raise Exception("get_namespace_for_site function can only be called if SITE_NAMESPACES is defined in the settings.")

    site = get_current_site()
    if site == None:
        return None
    try:
        return settings.SITE_NAMESPACES[site]
    except KeyError:
        raise KeyError("SITE_NAMESPACES setting has no key '%s'" % site)

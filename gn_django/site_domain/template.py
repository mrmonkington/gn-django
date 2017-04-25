import weakref

from .site_domains import get_current_site_domain

def get_template_cache_key_with_site_domain(loader, template_name):
    """
    Template cache key callback function which varies the cache key on the
    current site domain.

    To use it, the import string for this function should be set as the 
    `template_cache_key_cb` option in the jinja template backend setting in 
    `TEMPLATES`.
    """
    cache_key = (weakref.ref(loader), get_current_site_domain(), template_name)
    return cache_key

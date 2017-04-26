import weakref

from .site import get_current_site

def get_template_cache_key_with_site(loader, template_name):
    """
    Template cache key callback function which varies the cache key on the
    current site.

    To use it, the import string for this function should be set as the 
    `template_cache_key_cb` option in the jinja template backend setting in 
    `TEMPLATES`.
    """
    cache_key = (weakref.ref(loader), get_current_site(), template_name)
    return cache_key

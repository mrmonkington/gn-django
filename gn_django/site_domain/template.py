import weakref

from .site_domains import get_current_site_domain

def get_template_cache_key_with_site_domain(loader, template_name):
    cache_key = (weakref.ref(loader), get_current_site_domain(), template_name)
    return cache_key

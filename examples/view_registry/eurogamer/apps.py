from gn_django.app import GNAppConfig

from . import views

class EurogamerConfig(GNAppConfig):
    name = 'eurogamer'
    view_registry = {
        'core:Home': views.EurogamerHome,
    }

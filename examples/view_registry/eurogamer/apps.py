from gn_django.app import GNAppConfig

from . import views

class EurogamerConfig(GNAppConfig):
    name = 'eurogamer'
    views = {
        'core:Home': views.EurogamerHome,
    }

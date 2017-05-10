from gn_django.app import GNAppConfig

from . import views

class CoreConfig(GNAppConfig):
    name = 'core'
    views = {
        'core:ArchiveView': views.ArchiveView,
        'core:AboutView': views.AboutView,
    }

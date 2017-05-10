from gn_django.app import GNAppConfig

from . import views

class CoreConfig(GNAppConfig):
    name = 'core'
    view_registry = {
        'core:ArchiveView': views.ArchiveView,
        'core:AboutView': views.AboutView,
    }

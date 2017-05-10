from gn_django.app import GNAppConfig

from . import views

class ContentConfig(GNAppConfig):
    name = 'content'
    view_registry = {
        'core:AboutView': views.AboutView,
        'content:ArticleView': views.ArticleView,
    }

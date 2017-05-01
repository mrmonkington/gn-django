from gn_django.view import view_registry

from . import views

view_registry.register('content:ArticleView', views.ArticleView)
view_registry.register('core:AboutView', views.AboutView)

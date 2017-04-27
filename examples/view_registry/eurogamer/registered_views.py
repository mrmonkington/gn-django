from gn_django.view import view_registry

from . import views

view_registry.register('core:Home', views.EurogamerHome)


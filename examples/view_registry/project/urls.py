from django.conf.urls import url
from django.contrib import admin

from gn_django.view import view_registry

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view_registry.get('core:Home')),
]

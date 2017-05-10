from django.conf.urls import url
from django.contrib import admin

from gn_django.app import view_registry

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view_registry.get('core:Home')),
]

from django.urls import include, path
from django.contrib import admin

from django.views.generic import TemplateView

from .views import DomainView

from gn_django.app import view_registry

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', TemplateView.as_view(template_name="about.j2"), name="home"),
    path('site', DomainView.as_view()),
    path('archive', view_registry.get('core:ArchiveView')),
    path('about', view_registry.get('core:AboutView')),
    path('article', view_registry.get('content:ArticleView')),
    path('csv-link', view_registry.get('content:CsvDownloadLink')),
    path('csv-download', view_registry.get('content:CsvDownload')),
]

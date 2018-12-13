"""tests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.views.generic import TemplateView

from .views import DomainView

from gn_django.app import view_registry

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home', TemplateView.as_view(template_name="about.j2"), name="home"),
    url(r'^site', DomainView.as_view()),
    url(r'^archive', view_registry.get('core:ArchiveView')),
    url(r'^about', view_registry.get('core:AboutView')),
    url(r'^article', view_registry.get('content:ArticleView')),
    url(r'^csv-link', view_registry.get('content:CsvDownloadLink')),
    url(r'^csv-download', view_registry.get('content:CsvDownload')),
]

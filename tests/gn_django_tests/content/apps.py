from gn_django.app import GNAppConfig

from . import views

class ContentConfig(GNAppConfig):
    name = 'content'
    views = {
        'core:AboutView': views.AboutView,
        'content:ArticleView': views.ArticleView,
        'content:CsvDownloadLink': views.CsvDownloadLink,
        'content:CsvDownload': views.CsvDownload,
    }

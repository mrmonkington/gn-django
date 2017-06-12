from django.views.generic import TemplateView

from gn_django import helpers
from .models import ExampleModel
from gn_django.url import helpers as url_helpers
from gn_django.video import youtube

class Home(TemplateView):

    template_name = "home.j2"

    def get_context_data(self):
        return {'msg': helpers.super_helper()}

class Include(TemplateView):
    template_name = "include.j2"

    def get_context_data(self):
        return {
            'string': 'This is a message',
            'obj': ExampleModel('Hello World!'),
            'parent_context': 'Parent context',
        }

class Youtube(TemplateView):
    template_name = "youtube.j2"

    def get_context_data(self):
        url = 'https://www.youtube.com/watch?v=7pV5r4ePww8'

        return {
            'url': url,
            'id': youtube.get_id(url),
            'thumb': youtube.get_thumb(url),
            'alt_thumb': youtube.get_thumb(url, 2),
        }

class URLProtocol(TemplateView):
    template_name = 'url-protocol.j2'

    def get_context_data(self):
        http = 'http://www.eurogamer.net'
        https = 'https://www.usgamer.net'

        return {
            'http': http,
            'http_stripped': url_helpers.strip_protocol(http),
            'https': https,
            'https_stripped': url_helpers.strip_protocol(https),
        }

class StaticLinkExtension(TemplateView):
    template_name = 'static-link-extension.j2'

from django.views.generic import TemplateView

from gn_django import helpers
from gn_django.video import youtube

class Home(TemplateView):

    template_name = "home.html"

    def get_context_data(self):
        return {'msg': helpers.super_helper()}

class Youtube(TemplateView):
    template_name = "youtube.html"

    def get_context_data(self):
        url = 'https://www.youtube.com/watch?v=7pV5r4ePww8'

        return {
            'url': url,
            'id': youtube.get_id(url),
            'thumb': youtube.get_thumb(url),
            'alt_thumb': youtube.get_thumb(url, 2),
        }

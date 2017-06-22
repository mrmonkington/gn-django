from django.views.generic import TemplateView

from gn_django import utils

class Home(TemplateView):

    template_name = "home.j2"

    def get_context_data(self):
        return {'msg': utils.super_helper()}


class Article(TemplateView):

    template_name = "article.j2"

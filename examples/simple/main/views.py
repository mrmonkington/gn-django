from django.views.generic import TemplateView

from gn_django import helpers

class Home(TemplateView):

    template_name = "home.html"

    def get_context_data(self):
        return {'msg': helpers.super_helper()}

class Include(TemplateView):

    template_name = "include.html"

    def get_context_data(self):
        return {'msg': helpers.super_helper()}

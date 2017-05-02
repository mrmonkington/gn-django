from django.views.generic import TemplateView

from gn_django import helpers

class Home(TemplateView):

    template_name = "home.j2"

    def get_context_data(self):
        return {'msg': helpers.super_helper()}


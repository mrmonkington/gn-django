from django.views.generic import TemplateView

class Home(TemplateView):

    template_name = "home.j2"

    def get_context_data(self):
        return {'msg': "A message from core!", 'title': 'Welcome to the site'}


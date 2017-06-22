from django.views.generic import TemplateView

from core.views import Home

class EurogamerHome(Home):

    def get_context_data(self):
        # Override the message to be eurogamer specific
        context = super(EurogamerHome, self).get_context_data()
        context['msg'] = 'A message from eurogamer!'
        return context


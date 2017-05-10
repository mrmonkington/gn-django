from django.views.generic import TemplateView

class ArchiveView(TemplateView):

    template_name = "archive.html"

    def get_context_data(self):
        return {
            'app': 'core',
        }

class AboutView(TemplateView):

    template_name = "about.html"

    def get_context_data(self):
        return {
            'app': 'core',
        }

from django.views.generic import TemplateView

class ArchiveView(TemplateView):

    template_name = "archive.j2"

    def get_context_data(self):
        return {
            'app': 'core',
        }

class AboutView(TemplateView):

    template_name = "about.j2"

    def get_context_data(self):
        return {
            'app': 'core',
        }

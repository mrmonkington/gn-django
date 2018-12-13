from django.views.generic import TemplateView
from django.views.generic.base import View
from gn_django.utils import csv_download_response

class ArticleView(TemplateView):

    template_name = "article.j2"

    def get_context_data(self):
        return {
            'app': 'content',
        }

class AboutView(TemplateView):

    template_name = "about.j2"

    def get_context_data(self):
        return {
            'app': 'content',
        }

class CsvDownloadLink(TemplateView):
    template_name = "csv_download.j2"

class CsvDownload(View):
    def get(self, request):
        data = (
            ('Byte', '& Barq'),
            ('Dr', 'Coyle'),
            ('Hedlok', ''),
            ('Helix', ''),
            ('Kid', 'Cobra'),
            ('Lola', 'Pop'),
            ('Master', 'Mummy'),
            ('Max', 'Brass'),
            ('Mechanica', ''),
            ('Min', 'Min'),
            ('Misango', ''),
            ('Ninjara', ''),
            ('Ribbon', 'Girl'),
            ('Spring', 'Man'),
            ('Springtron', ''),
            ('Twintelle', ''),
        )
        response, writer = csv_download_response(('First Name', 'Second Name'), data, 'arms-roster')
        writer.writerow(('Biff', ''))
        return response

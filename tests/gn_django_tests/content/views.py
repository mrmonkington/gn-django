from django.views.generic import TemplateView

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

from django.views.generic import TemplateView

class ArticleView(TemplateView):

    template_name = "article.html"

    def get_context_data(self):
        return {
            'app': 'content',
        }

class AboutView(TemplateView):

    template_name = "about.html"

    def get_context_data(self):
        return {
            'app': 'content',
        }

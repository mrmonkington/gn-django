from django.apps import AppConfig

class GNAppConfig(AppConfig):
    """
    Gamer Network specific AppConfig class extending django's applications
    library (https://docs.djangoproject.com/en/1.11/ref/applications/).

    This currently offers a views dictionary for use with 
    ``gn_django.app.view_registry`` to allow django apps to register overridable
    view classes.
    """
    
    views = {}

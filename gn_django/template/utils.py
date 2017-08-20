import os

from django.template import loader

def render_to_string(template, context, request=None, using=None):
    """
    Shortcut for rendering templates using the current django project's collection
    of loaders.
    
    Args:
      * `template` - string - the template to render
      * `context` - mapping - the template context
    Kwargs:
      * `request` - HttpRequest - the current request, if available
      * `using` - 

    Returns:
      The rendered template string.
    """
    return loader.render_to_string(template, context=context, request=request, using=using)

def get_template_dir_for_app(app_name):
    """
    """
    app_module = __import__(app_name)
    app_path = os.path.dirname(app_module.__file__)
    template_path = os.path.join(app_path, 'templates')
    return template_path

from django.utils.module_loading import autodiscover_modules
from django.views.generic.base import View

"""
The view registry allows django apps to progressively override the class based
view that will service a particular url.

Using the registry means we do not need to duplicate url patterns in multiple
apps' `urls.py` files.

An app registers View classes to the registry in a `registered_views.py` file.
All apps' `registered_views.py` files are included when the django application 
is started - so long as `register_views` is called in the project's urls.py.
The view registry is populated in the order of `settings.INSTALLED_APPS` 
so that subsequent apps can override the views of preceding apps - this means
that apps lower in `INSTALLED_APPS` will override apps that are higher.

This enables the eurogamer_net app's `content:ArticleView` to override 
the content app's `content:ArticleView`, etc.
"""


_registry = {}

def _get_views_in_module(module):
    module_dict = module.__dict__
    views = [
        module_dict[c] for c in module_dict.keys() if (
            type(module_dict[c]) == type and
            issubclass(module_dict[c], View) and 
            module_dict[c].__module__ == module.__name__
        )
    ]
    return views

def _process_view_label(view_label):
    try:
        app, view_name = view_label.split(':')
    except ValueError:
        raise Exception("The view label should be of format '[app_name]:[view_class_name]'")
    return (app, view_name)

def register(view_label, view):
    """
    Register a django class based view for a particular view label string.

    Args:
      * ``view_label`` - string of format '[app_name]:[view_class_name]
      * ``view`` - django class based view
    """
    app, view_name = _process_view_label(view_label)
    try:
        _registry[app][view_name] = view.as_view()
    except KeyError:
        _registry[app] = {}
        _registry[app][view_name] = view.as_view()

def register_app_views(app, views_module):
    """
    Bulk register all of the class based views in a given module under an app 
    label namespace.
    This will automatically register all of the class based views found under 
    the `views_module` with their view class names.

    Args:
      * ``app`` - the app label to register under
      * ``views_module`` - a python module reference containing class based views.
    """
    views = _get_views_in_module(views_module)
    for view in views:
        view_label = ':'.join([app, view.__name__])
        register(view_label=view_label, view=view)
    

def get(view_label):
    """
    Retrieve the class based view for the view label of format 
    ``'[app_name]:[view_class_name]'``
    """
    app, view_name = _process_view_label(view_label)
    def _get_view(*args, **kwargs):
        try:
            return _registry[app][view_name](*args, **kwargs)
        except KeyError:
            raise KeyError("No class based view is registered for the label '%s'.  Is the app in INSTALLED_APPS?" % view_label)
    return _get_view

def register_views():
    """
    Go through all INSTALLED_APPS' ``registered_views.py`` modules and register
    the views.
    """
    autodiscover_modules('registered_views')

# Avoid a circular import by popping this at the bottom
register_views()

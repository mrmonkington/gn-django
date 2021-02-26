from functools import wraps

from django.views.generic.base import View
from django.apps import apps

from .app_config import GNAppConfig

"""
The view registry allows django apps to progressively override the class based
view that will service a particular url.

Using the registry means we do not need to duplicate url patterns in multiple
apps' `urls.py` files.

An app registers View classes to the registry by declaring a `GNAppConfig` 
subclass in `apps.py`.

All apps' app configs are iterated over to build the global view registry for
a django project.  This occurs the first time that a view is queried for using
the `get` function.
The view registry is populated in the order of `settings.INSTALLED_APPS` 
so that subsequent apps can override the views of preceding apps - this means
that apps lower in `INSTALLED_APPS` will override apps that are higher.

Example: This enables the eurogamer_net app's `content:ArticleView` to override 
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

def initialise_view_registry():
    """
    Goes through all installed apps which use GNAppConfig and have a non-empty
    view registry and initialises the project's view registry.

    Repeated calls will return the cached registry early if the global
    view registry is already populated.
    """
    if _registry:
        return
    all_apps = apps.get_app_configs()
    for app in all_apps:
        if isinstance(app, GNAppConfig):
            if not app.views:
                raise Exception(
                    f'No views were found in {app.__class__}. This may indicate '
                    'that views were initialised prematurely. Check that you '
                    'are not resolving URLs or any other actions that '
                    'initialise views before all apps are ready.'
                )
            for label, view in app.views.items():
                app, view_name = _process_view_label(label)
                try:
                    _registry[app][view_name] = view.as_view()
                except KeyError:
                    _registry[app] = {}
                    _registry[app][view_name] = view.as_view()

def get(view_label):
    """
    Retrieve the view callable for the view label of format
    ``'[app_name]:[view_class_name]'``

    Args:
      * ``view_label`` - string - view label of format `'[app_name]:[view_class_name]'`
    """
    app, view_name = _process_view_label(view_label)
    initialise_view_registry()
    view = _registry.get(app, {}).get(view_name)

    def wrapped_view(*args, **kwargs):
        if not view:
            raise KeyError(
                "No class based view is registered for the label '%s'.  Is "
                "the app in INSTALLED_APPS?" % view_label
            )
        return view(*args, **kwargs)

    return wraps(view)(wrapped_view)


def view_is_in_registry(view_label):
    """
    Check if a view with the given label exists in the view registry.

    Args:
      * `view_label` - string - view label of format
        `'[app_name]:[view_class_name]'`
    """
    initialise_view_registry()
    app, view_name = _process_view_label(view_label)
    return bool(_registry.get(app, {}).get(view_name))

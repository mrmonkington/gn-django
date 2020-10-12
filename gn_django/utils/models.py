from django.db.models import Model
from django.utils.text import slugify

from . import all_subclasses


def unique_object_slug(obj, source, slug_field='slug', limit=10000):
    """
    Utility for generating unique slugs based on a source string. For instance
    converting an article title of 'Bloodborne 2 Announced' to 'bloodborne-2-announced'.
    If the slug is already taken it will append a numeric value, i.e. 'bloodborne-2-announced-1'
    """
    if isinstance(obj, Model):
        model = obj.__class__
    elif issubclass(obj, Model):
        model = obj
    else:
        raise ValueError('Object is not a model or model class: %s' % repr(obj))

    base_slug = slugify(source)
    current_slug = base_slug
    search = '%s__startswith' % slug_field
    objects = model.objects.filter(**{search: base_slug})

    for i in range(1, limit):
        o = objects.filter(**{slug_field: current_slug})
        if (len(o) == 0) or (o[0].id == obj.id):
            return current_slug
        current_slug = '%s-%s' % (base_slug, i)

    return False


def super_receiver(signal, base_class, **kwargs):
    """
    A decorator for connecting receivers to signals for multiple senders.
    Works like the django.db.models.signals.receiver decorator, but will
    connect itself to all classes that inherit from the given base_class.

        @super_receiver(post_save, base_class=MyAbstractClass)
        def signal_receiver(sender, **kwargs):
            ...

        @super_receiver([post_save, post_delete], base_class=MyAbstractClass)
        def signals_receiver(sender, **kwargs):
            ...
    """
    def _decorator(func):
        signals = signal if isinstance(signal, (list, tuple)) else (signal,)
        for s in signals:
            for subclass in all_subclasses(base_class):
                s.connect(func, subclass, **kwargs)
        return func

    return _decorator

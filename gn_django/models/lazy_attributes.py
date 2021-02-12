import json
from collections.abc import MutableMapping
from django.core.exceptions import ValidationError


class LazyAttributes(MutableMapping):
    """
    Class to mock a dictionary on instances of ``LazyDictionaryMixin``.
    Instead of loading attributes on instantiation, it lazy loads them, so that the same set of
    attributes are not resolved multiple times.
    """
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self._attributes = None

    def __getitem__(self, key):
        self._load()
        return self._attributes.__getitem__(key)

    def __setitem__(self, key, value):
        self._load()
        self._attributes[key] = value

    def __delitem__(self, key):
        self._load()
        del self._attributes[key]

    def __iter__(self):
        self._load()
        return iter(self._attributes)

    def __len__(self):
        self._load()
        return len(self._attributes)

    def __repr__(self):
        self._load()
        return self._attributes.__repr__()

    def __contains__(self, key):
        self._load()
        return self._attributes.__contains__(key)

    def _load(self):
        if self._attributes is None:
            self._attributes = dict(self.parent.get_all_attributes().items())

    def reset(self):
        self._attributes = None


class LazyAttributesMixin:
    """
    Mixin for models to allow for overridable attributes. The top level class should
    declare its attributes under `self.attributes`. Every non-parent class
    should declare the attributes under `self.override_attributes`. Non-parent classes
    should call `_setup_attributes()` within its `__init__()` method. Note, this mixin
    cannot declare its own `__init__()` method as this will break Django models.
    """

    parent = None

    """
    Store attributes in memory until they are re-written. This prevents multiple
    queries being run for the same object unnecessarily
    TODO: Move this to general purpose object cache, when it exists
    """
    attribute_cache = {}

    # def __init__(self, *args, **kwargs):
    #     It's pretty tempting to put an __init__() method here so that we don't need to call
    #     `_setup_attributes()` on the individual models. Well if you try that you'll
    #     get weird errors when trying to use this with Django's models since Django doesn't
    #     like you to mess around with its __init__ methods.

    def get_attribute(self, name):
        try:
            return self.attributes[name]
        except KeyError:
            return self.parent.get_attribute(name)

    def get_all_attributes(self, as_json=False):
        """
        Get all attributes that apply to this model. This includes all attributes of
        parent objects that have not been overridden by objects further down in the chain.
        """
        attributes = {}

        if hasattr(self, 'override_attributes'):
            attributes = self.override_attributes

        # Top level models will not have a parent
        if self.parent:
            attributes = {**self.parent.attributes, **attributes}

        if as_json:
            attributes = json.dumps(attributes, indent=True)
        return attributes

    def get_inherited_attributes(self, as_json=False):
        """
        Get all attributes which belong to parents, without attributes specific to this object.
        """
        inherited = {}
        for k, v in self.attributes.items():
            if k not in self.override_attributes:
                inherited[k] = v
        if as_json:
            inherited = json.dumps(inherited, indent=True)
        return inherited

    def save(self, *args, **kwargs):
        """
        Clean up the object before saving
        """
        self.clean_attributes()
        super().save(*args, **kwargs)

    def clean_attributes(self):
        """
        Remove attributes which belong to parent objects from the overrides
        """
        if not self.parent:
            return
        self.override_attributes = dict(self.attributes)
        dupes = []
        for k, v in self.override_attributes.items():
            if k in self.parent.attributes and v == self.parent.attributes[k]:
                dupes.append(k)
        for k in dupes:
            del self.override_attributes[k]
        self._setup_attributes()

    def _setup_attributes(self):
        if not hasattr(self.__class__, 'attributes'):
            self.attributes = LazyAttributes(parent=self)

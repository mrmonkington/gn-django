from collections import OrderedDict

from django.utils import six
from django.utils.module_loading import import_string
from jinja2.loaders import BaseLoader, TemplateNotFound, iteritems, FileSystemLoader

"""
Custom template loaders that can be used for special template loading 
functionality.
"""

class DjangoTemplateNotFound(TemplateNotFound):
    
    def __init__(self, name, message=None, tried=None):
        super(DjangoTemplateNotFound, self).__init__(name, message)
        if tried:
            self.tried = tried

class JinjaOrigin(object):
    def __init__(self, loader, name):
        self.loader_name = loader.__class__.__name__
        self.name = name


class NamespaceLoader(BaseLoader):
    """
    A loader that is a combination of the PrefixLoader and ChoiceLoader.
    If there's a prefix, use that loader, otherwise go through all Loaders until
    a match is found.

    Takes an OrderedDict loader mapping with keys of loader names and values
    of instantiated `Loader` objects.  This mapping should be in order of most
    specific (concrete) template to least specific (parent/base) template.

    Allows three formats of template lookup:

    - `app_parent:base.html` - dynamic lookup - this will attempt to find
       the closest ancestor template that matches below the loader named `app`
       in the loader mapping.

    - `core:base.html` - directed lookup - this will attempt to find the `base.html`
       template in the loader called `core` in the loader mapping.

    - `base.html` - sequential lookup - this will attempt to find the `base.html`
       template by trying all of the loaders in the loader mapping, sequentially.
       Note: If the other two methods fail, sequential lookup is the fallback.

    Say that we have a loader mapping as follows:
        ```
        loaders = OrderedDict({
            'eurogamer': Loader(),
            'editorial': Loader(),
            'core': Loader(),
        })
        choice_loader = NamespaceLoader(loaders)

        choice_loader.get_source(env, 'editorial_parent:base.html')
        ```
        Will yield `base.html` from the `'core'` loader and will
        otherwise try to find it sequentially from eurogamer to core.

        ```
        choice_loader.get_source(env, 'core:foo.html')
        ```
        Will yield `foo.html` from the `'core'` loader if it exists and will
        otherwise try to find it sequentially from eurogamer to core.

        ```
        choice_loader.get_source(env, 'bar.html')
        ```
        Will find `bar.html` by querying the loaders sequentially from eurogamer
        to core.
    """

    def __init__(self, mapping, delimiter=':'):
        if not isinstance(mapping, OrderedDict):
            raise Exception("NamespaceLoader must be called with a \
                collections.OrderedDict type of mapping")
        self.mapping = mapping
        self.delimiter = delimiter

    def get_ancestor_loader_names(self, child):
        """
        Get a list of ancestor loaders to try, in order of closest relative to 
        most distant.
        """
        # Get a list of loader keys
        all_loaders = list(self.mapping)
        try:
            child_index = all_loaders.index(child)
        except ValueError:
            raise TemplateNotFound()
        return all_loaders[child_index+1:]

    def get_parent_template(self, environment, template, tried):
        """
        Given a template identifier of format `<app>_parent:foo.html` find the
        template by going through the loaders above it sequentially until it is
        found.

        Raises `TemplateNotFound`
        """
        try:
            prefix, template_name = template.split(self.delimiter, 1)
        except ValueError:
            raise TemplateNotFound(template)
        try:
            child = prefix.split("_parent", 1)[0]
        except ValueError:
            raise TemplateNotFound(template)
        loader_ancestry = self.get_ancestor_loader_names(child)
        for loader_name in loader_ancestry:
            loader = self.mapping[loader_name]
            try:
                return loader.get_source(environment, template_name)
            except TemplateNotFound:
                loader_path = "%s/%s" % (loader.searchpath[0], template)
                origin = JinjaOrigin(loader, loader_path)
                tried.append([origin, "Source does not exist"])
                continue
        raise TemplateNotFound(template)
        
    def get_loader(self, template):
        try:
            prefix, name = template.split(self.delimiter, 1)
        except ValueError:
            raise TemplateNotFound(template)
        try:
            loader = self.mapping[prefix]
        except (KeyError):
            raise TemplateNotFound(template)
        return loader, name

    def get_source(self, environment, template):
        # Try to find the parent template if it exists
        tried = []
        if self.delimiter in template and "_parent:" in template:
            try:
                return self.get_parent_template(environment, template, tried)
            except TemplateNotFound:
                pass
        # Try to load from a named loader if the template string is prefixed with one
        if self.delimiter in template:
            loader, name = self.get_loader(template)
            try:
                return loader.get_source(environment, name)
            except TemplateNotFound:
                pass
        # Otherwise, go through the all template loaders until we find one that matches
        for loader_name, loader in self.mapping.items():
            try:
                return loader.get_source(environment, template)
            except TemplateNotFound:
                loader_path = "%s/%s" % (loader.searchpath[0], template)
                origin = JinjaOrigin(loader, loader_path)
                tried.append([origin, "Source does not exist"])
                continue
        raise DjangoTemplateNotFound(template, tried=tried)

    def list_templates(self):
        result = []
        for prefix, loader in iteritems(self.mapping):
            for template in loader.list_templates():
                result.append(prefix + self.delimiter + template)
        return result

def get_static_namespace_loader(directories):
    template_loaders = OrderedDict()
    for app_name, template_dir in directories:
        template_loaders[app_name] = FileSystemLoader(template_dir)
    return NamespaceLoader(template_loaders)


class MultiNamespaceLoader(BaseLoader):

    def __init__(self, get_active_namespace_cb, mapping, delimiter=':'):
        self.get_active_namespace_cb = get_active_namespace_cb
        self.mapping = mapping
        self.delimiter = delimiter

    def get_loader(self):
        if isinstance(self.get_active_namespace_cb, six.string_types):
            self.get_active_namespace_cb = import_string(self.get_active_namespace_cb)
        namespace = self.get_active_namespace_cb()
        return self.mapping[namespace]

    def get_source(self, environment, template):
        current_loader = self.get_loader()
        return current_loader.get_source(environment, template)

    def list_templates(self):
        result = []
        for prefix, loader in iteritems(self.mapping):
            for template in loader.list_templates():
                result.append(prefix + self.delimiter + template)
        return result

def get_multi_namespace_loader(get_active_namespace_cb, namespaces):
    template_loaders = {}
    for namespace_name, directories in namespaces:
        template_loaders[namespace_name] = get_static_namespace_loader(directories)
    return MultiNamespaceLoader(get_active_namespace_cb, template_loaders)

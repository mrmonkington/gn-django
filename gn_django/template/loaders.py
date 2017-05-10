from collections import OrderedDict

from django.utils import six
from django.utils.module_loading import import_string
from jinja2.loaders import BaseLoader, TemplateNotFound, iteritems, FileSystemLoader

"""
Custom template loaders that can be used for special template loading 
functionality.
"""

class DjangoTemplateNotFound(TemplateNotFound):
    """
    Adds a `tried` attribute to our `TemplateNotFound` exception - which allows
    django to flag the template locations that were attempted.
    """
    
    def __init__(self, name, message=None, tried=None):
        super(DjangoTemplateNotFound, self).__init__(name, message)
        if tried:
            self.tried = tried

class JinjaOrigin(object):
    def __init__(self, loader, name):
        self.loader_name = loader.__class__.__name__
        self.name = name


class HierarchyLoader(BaseLoader):
    """
    A loader that is a combination of the PrefixLoader and ChoiceLoader.
    This allows us to define a hierarchy of template loaders such that a 
    template defined in the most specific part of the hierarchy is loaded in
    preference to a template in the least specific part of the hierarchy.  This
    enables very granular overrides of templates and finer control of template 
    loading through various lookup modes determined by prefixing the template
    name.

    Takes an ``OrderedDict`` loader hierarchy with keys as loader names and values
    as instantiated `Loader` objects.  This mapping should be in order of most
    specific (concrete) template loader to least specific (parent/base) 
    template loader.

    Allows three formats of template lookup:

      * ``<loader>_parent:base.html`` - ancestor lookup - this will attempt to find
        the closest ancestor template that matches below the named loader
        in the loader hierarchy.

      * ``<loader>:base.html`` - namespace lookup - this will attempt to find the `base.html`
        template from the specified named loader in the loader hierarchy.

      * ``base.html`` - sequential lookup - this will attempt to find the `base.html`
        template by trying all of the loaders in the loader hierarchy, sequentially.

    Say that we have a loader hierarchy as follows::

        loaders = OrderedDict({
            'eurogamer_net': Loader(),
            'eurogamer': Loader(),
            'core': Loader(),
        })
        hierarchy_loader = HierarchyLoader(loaders)

        hierarchy_loader.get_source(env, 'eurogamer_parent:base.html')

    Will yield `base.html` from the `'core'` loader and will
    otherwise try to find it sequentially from eurogamer to core::

        hierarchy_loader.get_source(env, 'core:foo.html')

    Will yield `foo.html` from the `'core'` loader if it exists and will
    otherwise try to find it sequentially from the ``eurogamer`` loader to ``core``::

        hierarchy_loader.get_source(env, 'bar.html')

    Will find `bar.html` by querying the loaders sequentially from ``eurogamer_net``
    to ``core``.
    """

    def __init__(self, hierarchy, delimiter=':'):
        """
        Args:
          * `hierarchy` - OrderedDict - ordered dict with keys as template
            namespace and values as template loader, in order of most specific
            to least specific.
          * `delimiter` - string - the namespace delimiter string to use when
            separating namespace from template identifier
        """
        if not isinstance(hierarchy, OrderedDict):
            raise Exception("HierarchyLoader must be called with a \
                collections.OrderedDict type of mapping")
        self.hierarchy = hierarchy
        self.delimiter = delimiter

    def identify_loading_mode(self, template_name):
        """
        Given a template identifier string, work out the loading mode to use as
        either ancestor, namespace or sequential.

        Args:
          * `template_name` - string - the template name to identify the loading
            mode for.
        """
        if self.delimiter in template_name and "_parent:" in template_name:
            return "ancestor"
        if self.delimiter in template_name:
            return "namespace"
        return "sequential"

    def get_ancestor_loader_names(self, child):
        """
        Get a list of ancestor loaders to try, in order of closest relative to 
        most distant.
        """
        # Get a list of loader keys
        all_loaders = list(self.hierarchy)
        try:
            child_index = all_loaders.index(child)
        except ValueError:
            raise TemplateNotFound()
        return all_loaders[child_index+1:]

    def get_ancestor_source(self, environment, template, tried):
        """
        Given a template identifier of format `<loader>_parent:foo.html` find the
        template by going through the loaders above it sequentially until it is
        found.

        Args:
          * `environment` - the jinja environment object
          * `template` - the template name to look up
          * `tried` - ref to iterable of tried paths

        Raises `TemplateNotFound`
        Returns an instantiated template
        """
        try:
            prefix, template_name = template.split(self.delimiter, 1)
        except ValueError:
            raise TemplateNotFound(template)
        try:
            child = prefix.split("_parent", 1)[0]
        except ValueError:
            raise TemplateNotFound(template)
        # Work out a flat list of the loader's ancestry to iterate through
        loader_ancestry = self.get_ancestor_loader_names(child)
        # For each loader in the ancestry, try to get the template and return it
        for loader_name in loader_ancestry:
            loader = self.hierarchy[loader_name]
            try:
                return loader.get_source(environment, template_name)
            except TemplateNotFound:
                loader_path = "%s/%s" % (loader.searchpath[0], template)
                origin = JinjaOrigin(loader, loader_path)
                tried.append([origin, "Source does not exist"])
                continue
        raise TemplateNotFound(template)

    def get_namespace_source(self, environment, template, tried):
        """
        Given a template identifier of format `<loader>:foo.html` find the
        template by looking up the specified loader in the loader hierarchy and 
        retrieving it from there.

        Args:
          * `environment` - the jinja environment object
          * `template` - the template name to look up
          * `tried` - ref to iterable of tried paths

        Raises `TemplateNotFound`
        Returns an instantiated template
        """
        try:
            loader_name, template_name = template.split(self.delimiter, 1)
        except ValueError:
            raise TemplateNotFound(template)
        try:
            loader = self.hierarchy[loader_name]
        except (KeyError):
            raise TemplateNotFound(template)
        return loader.get_source(environment, template_name)

    def get_sequential_source(self, environment, template, tried):
        """
        Given a template name, find the template by going through the loader
        ancestry sequentially from most specific to least specific.

        Args:
          * `environment` - the jinja environment object
          * `template` - the template name to look up
          * `tried` - ref to iterable of tried paths

        Returns an instantiated template or None if it could not be found
        """
        for loader_name, loader in self.hierarchy.items():
            try:
                return loader.get_source(environment, template)
            except TemplateNotFound:
                loader_path = "%s/%s" % (loader.searchpath[0], template)
                origin = JinjaOrigin(loader, loader_path)
                tried.append([origin, "Source does not exist"])
                continue
        return None
        
    def get_source(self, environment, template):
        """
        Get the template source for a given template identifier.  An appropriate
        loader is used based on whether the template identifier indicates 
        sequential, ancestor or namespace lookup modes.

        Args:
          * `environment` - the jinja environment object
          * `template` - the template name to look up
        """
        # Identify the loading mode from the template identifier
        loading_mode = self.identify_loading_mode(template)
        loading_method = getattr(self, "get_%s_source" % loading_mode)
        tried = []
        template_source = None
        # Attempt to use the identified loading mode to get the template source
        try:
            template_source = loading_method(environment, template, tried)
        except TemplateNotFound:
            pass

        # Return the template source if we managed to look it up successfully,
        # or raise a DjangoTemplateNotFound exception
        if template_source:
            return template_source
        else:
            raise DjangoTemplateNotFound(template, tried=tried)
            
    def list_templates(self):
        result = []
        for prefix, loader in iteritems(self.hierarchy):
            for template in loader.list_templates():
                result.append(prefix + self.delimiter + template)
        return result

def get_hierarchy_loader(directories):
    """
    Helper to instantiate a `HierarchyLoader` from a hierarchy of named directories.

    Args:
      * `directories` - iterable of pairs - The loader hierarchy to create; this
        should specify the name and directory for each loader in the
        hierarchy.  If we have "eurogamer_net", "eurogamer" and core in order of
        most to least specific, we should have the following:
        ```
            directories = (
                ("eurogamer_net", '/path/to/eurogamer_net'),
                ("eurogamer", '/path/to/eurogamer'),
                ("core", '/path/to/core'),
            )
        ```

    Returns an instantiated `HierarchyLoader()` object
    """
    template_loaders = OrderedDict()
    for app_name, template_dir in directories:
        template_loaders[app_name] = FileSystemLoader(template_dir)
    return HierarchyLoader(template_loaders)


class MultiHierarchyLoader(BaseLoader):
    """
    A loader composed of one or more ``HierarchyLoader`` objects.  The chosen
    hierarchy to use when loading a given template is determined by a callback
    function which is parameterised at object instantiation.

    Args:
      * `get_active_hierarchy_cb` - function/import string - import string of the function 
        to call to determine the hierarchy loader which is active right now.
      * `hierarchies` - mapping - mapping of hierarchy names to instantiated
        ``HierarchyLoader`` objects
    """

    def __init__(self, get_active_hierarchy_cb, hierarchies, delimiter=':'):
        self.get_active_hierarchy_cb = get_active_hierarchy_cb
        self.hierarchies = hierarchies
        self.delimiter = delimiter

    def get_loader(self):
        # Call the active hierarchy callback to determine the hierarchy loader
        # which is active right now
        if isinstance(self.get_active_hierarchy_cb, six.string_types):
            self.get_active_hierarchy_cb = import_string(self.get_active_hierarchy_cb)
        hierarchy = self.get_active_hierarchy_cb()
        return self.hierarchies[hierarchy]

    def get_source(self, environment, template):
        # Determine the currently active loader and get the template source from it
        current_loader = self.get_loader()
        return current_loader.get_source(environment, template)

    def list_templates(self):
        result = []
        for prefix, loader in iteritems(self.hierarchies):
            for template in loader.list_templates():
                result.append(prefix + self.delimiter + template)
        return result

def get_multi_hierarchy_loader(get_active_hierarchy_cb, hierarchies):
    """
    Helper to instantiate a ``MultiHierarchyLoader`` from many named template 
    directory hierarchies.

    Args:
      * `get_active_hierarchy_cb` - function/import string -  function 
        to call to determine the name of the hierarchy loader which is active 
        at any time.
      * `hierarchy` - iterable of pairs - The loader hierarchies to create.
        Each pair should specify the hierarchy name and template hierarchy for
        all template hierarchies to create.
        e.g.
        ```
            hierarchies = (
                ('eurogamer_net', (
                    ('eurogamer_net', os.path.join(TEMPLATE_BASE, 'eurogamer_net')),
                    ('eurogamer', os.path.join(TEMPLATE_BASE, 'eurogamer')),
                    ('core', os.path.join(TEMPLATE_BASE, 'core')),
                )),
                ('eurogamer_de', (
                    ('eurogamer_de', os.path.join(TEMPLATE_BASE, 'eurogamer_de')),
                    ('eurogamer', os.path.join(TEMPLATE_BASE, 'eurogamer')),
                    ('core', os.path.join(TEMPLATE_BASE, 'core')),
                )),
                ('vg247_com', (
                    ('vg247_com', os.path.join(TEMPLATE_BASE, 'vg247_com')),
                    ('vg247', os.path.join(TEMPLATE_BASE, 'vg247')),
                    ('core', os.path.join(TEMPLATE_BASE, 'core')),
                )),
                ('vg247_pl', (
                    ('vg247_pl', os.path.join(TEMPLATE_BASE, 'vg247_pl')),
                    ('vg247', os.path.join(TEMPLATE_BASE, 'vg247')),
                    ('core', os.path.join(TEMPLATE_BASE, 'core')),
                )),
            )
        ```

    Returns an instantiated ``MultiHierarchyLoader()`` object
    """
    template_loaders = {}
    for hierarchy_name, directories in hierarchies:
        template_loaders[hierarchy_name] = get_hierarchy_loader(directories)
    return MultiHierarchyLoader(get_active_hierarchy_cb, template_loaders)

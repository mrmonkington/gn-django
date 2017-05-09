import tempfile, os
from collections import OrderedDict
from unittest import mock

from jinja2.ext import Extension
from jinja2 import nodes
from jinja2.loaders import FileSystemLoader
from django.test import TestCase
from django.template.exceptions import TemplateDoesNotExist

from gn_django.template.backend import Jinja2
from gn_django.template.loaders import HierarchyLoader, get_hierarchy_loader
from gn_django.template.loaders import MultiHierarchyLoader, get_multi_hierarchy_loader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class TestJinja2(TestCase):
    """
    Tests for the Jinja2 class.
    """

    def get_jinja_config(self):
        params = {
            "APP_DIRS": True,
            "OPTIONS": {
                'match_extension': None,
                'context_processors': [
                    'gn_django.template.context_processors.settings',
                ],
            },
            "NAME": "djangojinja",
            "DIRS": [],
        }
        return params

    def test_templates_render(self):
        """
        Test that templates render.
        """
        jinja = Jinja2(self.get_jinja_config())
        template = jinja.from_string("<html>{{foo}}</html>")
        rendered = template.render({'foo': 'bar'})
        self.assertEqual("<html>bar</html>", rendered)

    def test_filters_work(self):
        """
        Test that filters work from a variety of sources.
        """
        test_cases = [
            # Vanilla jinja
            ['{{ "%s - %s"|format("Hello?", "Foo!") }}', "Hello? - Foo!"],
            # Django
            ['{{ "django"|capfirst }}', "Django"],
            # Django humanize
            ['{{ 20|ordinal }}', "20th"],
            # Custom from gn-django..
            # Defined in settings config...
            ['{{ 20|pointless }}', "pointless"],
        ]
        jinja_config = self.get_jinja_config()
        jinja_config['OPTIONS']['filters'] = {'pointless': lambda x: "pointless"}
        jinja = Jinja2(jinja_config)
        for template_str, expected_result in test_cases:
            template = jinja.from_string(template_str)
            rendered = template.render()
            self.assertEqual(rendered, expected_result)

    def test_globals_work(self):
        """
        Test that globals work from a variety of sources.
        """
        test_cases = [
            # Vanilla jinja
            ['{% for i in range(10) %}{{i}}{% endfor %}', "0123456789"],
            # Django
            ['{{ url("home") }}', "/home"],
            ['{{ static("js/lib/foo.js") }}', "/static/js/lib/foo.js"],
            # Custom from gn-django..
            # Defined in settings config...
            ['{{ pointless(1) }}', "pointless"],
        ]
        jinja_config = self.get_jinja_config()
        jinja_config['OPTIONS']['globals'] = {'pointless': lambda x: "pointless"}
        jinja = Jinja2(jinja_config)
        for template_str, expected_result in test_cases:
            template = jinja.from_string(template_str)
            rendered = template.render()
            self.assertEqual(rendered, expected_result)

    def test_extensions_work(self):
        """
        Test that extensions work from a variety of sources.
        """
        test_cases = [
            # Defaults from gn-django
            ['{% with a="foo" %}{{a}} bar{% endwith %}', "foo bar"],
            # Custom from gn-django..
            ['{% spaceless %} <div>a b c </div>    <div>d</div>{% endspaceless %}', "<div>a b c </div><div>d</div>"],
            # Defined in settings config...
            ['{% pointless %}', "pointless"],
        ]
        jinja_config = self.get_jinja_config()

        class PointlessExtension(Extension):
            """
            A dummy extension to register.
            """
            tags = set(['pointless'])
            def parse(self, parser):
                lineno = next(parser.stream).lineno
                return nodes.CallBlock(
                    self.call_method('_pointless', [], [], None, None),
                    [], [], [],
                ).set_lineno(lineno)

            def _pointless(self, caller=None):
                return "pointless"

        jinja_config['OPTIONS']['extensions'] = [PointlessExtension]
        jinja = Jinja2(jinja_config)
        for template_str, expected_result in test_cases:
            template = jinja.from_string(template_str)
            rendered = template.render()
            self.assertEqual(rendered, expected_result)

    def test_context_processors_work(self):
        """
        Test that context processors work.
        """
        test_cases = [
            # django settings context processor
            ['{{ settings.TIME_ZONE }}', "UTC"],
        ]
        jinja_config = self.get_jinja_config()
        jinja = Jinja2(jinja_config)
        for template_str, expected_result in test_cases:
            template = jinja.from_string(template_str)
            # Mocked (truthy) request
            rendered = template.render(request=True)
            self.assertEqual(rendered, expected_result)

    def test_include_with_extension(self):
        class ExampleModel:

            display_text = 'This is text that belongs to a model'

            def __init__(self, name):
                self.name = name

        template_dir = os.path.join(BASE_DIR, "test_files", "include_with_templates")

        jinja_config = self.get_jinja_config()
        jinja_config['DIRS'].append(template_dir)
        jinja = Jinja2(jinja_config)
        params = {
            'string': 'This is a message',
            'obj': ExampleModel('Hello World!'),
            'parent_context': 'Parent context',
        }

        result = jinja.get_template('include.html').render(params).strip()
        expected = jinja.get_template('include_expected.html').render().strip()

        self.assertEquals(result, expected)

class TestHierarchyLoader(TestCase):
    """
    Tests for the HierarchyLoader class.
    """

    def get_template_dir(self, dirname):
        template_base = os.path.join(BASE_DIR, "test_files", "sparse_templates")
        return os.path.join(template_base, dirname)

    def get_jinja_config(self):
        hierarchy = OrderedDict((
            ("eurogamer_net", FileSystemLoader(self.get_template_dir("eurogamer_net"))),
            ("eurogamer", FileSystemLoader(self.get_template_dir("eurogamer"))),
            ("core", FileSystemLoader(self.get_template_dir("core"))),
        ))
        loader = HierarchyLoader(hierarchy)
        params = {
            "APP_DIRS": True,
            "OPTIONS": {
                'match_extension': None,
                'context_processors': [
                    'gn_django.template.context_processors.settings',
                ],
                'loader': loader,
            },
            "NAME": "djangojinja",
            "DIRS": [],
        }
        return params

    def test_get_template_sequential(self):

        # Get a handle on the template engine
        jinja_config = self.get_jinja_config()
        jinja = Jinja2(jinja_config)

        # Test that the loader falls back to the least specific template
        # in the hierarchy
        t = jinja.get_template("base.html")
        self.assertEquals(t.template.filename, self.get_template_dir("core/base.html"))

        # Test that the loader picks up a template in the middle of the hierarchy
        t = jinja.get_template("article.html")
        self.assertEquals(t.template.filename, self.get_template_dir("eurogamer/article.html"))

        # Test that the loader picks up a template at the top of the hierarchy
        t = jinja.get_template("widgets/comments.html")
        self.assertEquals(t.template.filename, self.get_template_dir("eurogamer_net/widgets/comments.html"))

    def test_get_template_ancestor(self):
        # Get a handle on the template engine
        jinja_config = self.get_jinja_config()
        jinja = Jinja2(jinja_config)

        # Test that the loader can find parent templates from immediate ancestors
        t = jinja.get_template("eurogamer_net_parent:article.html")
        self.assertEquals(t.template.filename, self.get_template_dir("eurogamer/article.html"))

        # Test that the loader can find parent templates from non-immediate ancestors
        t = jinja.get_template("eurogamer_net_parent:base.html")
        self.assertEquals(t.template.filename, self.get_template_dir("core/base.html"))

        # Test that the loader can find parent templates when the template name
        # collides with a template available in the child namespace
        t = jinja.get_template("eurogamer_net_parent:widgets/comments.html")
        self.assertEquals(t.template.filename, self.get_template_dir("core/widgets/comments.html"))

    def test_get_template_directed(self):
        # Get a handle on the template engine
        jinja_config = self.get_jinja_config()
        jinja = Jinja2(jinja_config)

        # Test that the loader can find templates from a directed identifier
        t = jinja.get_template("core:article.html")
        self.assertEquals(t.template.filename, self.get_template_dir("core/article.html"))
        t = jinja.get_template("eurogamer_net:widgets/comments.html")
        self.assertEquals(t.template.filename, self.get_template_dir("eurogamer_net/widgets/comments.html"))

    def test_get_template_missing(self):
        # Get a handle on the template engine
        jinja_config = self.get_jinja_config()
        jinja = Jinja2(jinja_config)

        # Test that the loader raises an error when the template does not exist
        self.assertRaises(TemplateDoesNotExist, jinja.get_template, ("wibble.html"))
        self.assertRaises(TemplateDoesNotExist, jinja.get_template, ("core:wibble.html"))
        self.assertRaises(TemplateDoesNotExist, jinja.get_template, ("eurogamer_parent:wibble.html"))


class TestMultiHierarchyLoader(TestCase):
    """
    Tests for the HierarchyLoader class.
    """

    def get_template_dir(self, dirname):
        template_base = os.path.join(BASE_DIR, "test_files", "multi_hierarchy_sparse_templates")
        return os.path.join(template_base, dirname)

    def get_jinja_config(self, active_hierarchy_cb):
        multi_hierarchy = {
            'eurogamer_net': HierarchyLoader(
                OrderedDict((
                    ("eurogamer_net", FileSystemLoader(self.get_template_dir("eurogamer_net"))),
                    ("eurogamer", FileSystemLoader(self.get_template_dir("eurogamer"))),
                    ("core", FileSystemLoader(self.get_template_dir("core"))),
                ))
            ),
            'eurogamer_de': HierarchyLoader(
                OrderedDict((
                    ("eurogamer_de", FileSystemLoader(self.get_template_dir("eurogamer_de"))),
                    ("eurogamer", FileSystemLoader(self.get_template_dir("eurogamer"))),
                    ("core", FileSystemLoader(self.get_template_dir("core"))),
                ))
            ),
            'vg247_com': HierarchyLoader(
                OrderedDict((
                    ("vg247_com", FileSystemLoader(self.get_template_dir("vg247_com"))),
                    ("vg247", FileSystemLoader(self.get_template_dir("vg247"))),
                    ("core", FileSystemLoader(self.get_template_dir("core"))),
                ))
            ),
            'vg247_pl': HierarchyLoader(
                OrderedDict((
                    ("vg247_pl", FileSystemLoader(self.get_template_dir("vg247_pl"))),
                    ("vg247", FileSystemLoader(self.get_template_dir("vg247"))),
                    ("core", FileSystemLoader(self.get_template_dir("core"))),
                ))
            ),
        }
        loader = MultiHierarchyLoader(active_hierarchy_cb, multi_hierarchy)
        params = {
            "APP_DIRS": True,
            "OPTIONS": {
                'match_extension': None,
                'context_processors': [
                    'gn_django.template.context_processors.settings',
                ],
                'loader': loader,
            },
            "NAME": "djangojinja",
            "DIRS": [],
        }
        return params

    def run_test_cases(self, test_cases):
        for hierarchy_name, template_name, expected_template_location in test_cases:
            get_current_hierarchy_cb = mock.Mock(return_value=hierarchy_name)
            # Get a handle on the template engine
            jinja_config = self.get_jinja_config(get_current_hierarchy_cb)
            jinja = Jinja2(jinja_config)
            t = jinja.get_template(template_name)
            self.assertEquals(t.template.filename, expected_template_location)

    def test_get_template_sequential(self):
        test_cases = (
            ('eurogamer_net', 'base.html', self.get_template_dir('core/base.html')),
            ('eurogamer_net', 'widgets/comments.html', self.get_template_dir('eurogamer_net/widgets/comments.html')),
            ('eurogamer_de', 'base.html', self.get_template_dir('core/base.html')),
            ('eurogamer_de', 'article.html', self.get_template_dir('eurogamer/article.html')),
            ('vg247_com', 'base.html', self.get_template_dir('core/base.html')),
        )
        self.run_test_cases(test_cases)

    def test_get_template_ancestor(self):
        test_cases = (
            ('eurogamer_net', 'eurogamer_net_parent:base.html', self.get_template_dir('core/base.html')),
            ('eurogamer_net', 'eurogamer_net_parent:article.html', self.get_template_dir('eurogamer/article.html')),
            ('eurogamer_de', 'eurogamer_de_parent:base.html', self.get_template_dir('core/base.html')),
            ('eurogamer_de', 'eurogamer_de_parent:article.html', self.get_template_dir('eurogamer/article.html')),
            ('vg247_com', 'vg247_parent:base.html', self.get_template_dir('core/base.html')),
        )
        self.run_test_cases(test_cases)

    def test_get_template_directed(self):
        test_cases = (
            ('eurogamer_net', 'core:base.html', self.get_template_dir('core/base.html')),
            ('eurogamer_net', 'eurogamer:article.html', self.get_template_dir('eurogamer/article.html')),
            ('eurogamer_de', 'core:base.html', self.get_template_dir('core/base.html')),
            ('eurogamer_de', 'eurogamer:article.html', self.get_template_dir('eurogamer/article.html')),
            ('vg247_com', 'core:home.html', self.get_template_dir('core/home.html')),
        )
        self.run_test_cases(test_cases)

class TestLoaderBuilders(TestCase):
    """
    Tests for the loader builder functions.
    """

    def get_template_dir(self, dirname):
        template_base = os.path.join(BASE_DIR, "test_files", "sparse_templates")
        return os.path.join(template_base, dirname)

    def test_get_hierarchy_loader(self):
        expected_hierarchy = OrderedDict((
            ("eurogamer_net", FileSystemLoader(self.get_template_dir("eurogamer_net"))),
            ("eurogamer", FileSystemLoader(self.get_template_dir("eurogamer"))),
            ("core", FileSystemLoader(self.get_template_dir("core"))),
        ))
        loader = get_hierarchy_loader((
            ('eurogamer_net', self.get_template_dir('eurogamer_net')),
            ('eurogamer', self.get_template_dir('eurogamer')),
            ('core', self.get_template_dir('core')),
        ))
        expected_hierarchy_chain = list(expected_hierarchy.keys())
        expected_hierarchy_len = len(expected_hierarchy_chain)
        actual_hierarchy_chain = list(loader.hierarchy.keys())
        for i in range(expected_hierarchy_len):
            # Make sure the hierarchy is in the expected order
            loader_name = actual_hierarchy_chain[i]
            self.assertEquals(expected_hierarchy_chain[i], actual_hierarchy_chain[i])
            # Make sure the templates contained within the built loader is
            # identical to what we are expecting
            expected_templates = expected_hierarchy[loader_name].list_templates()
            actual_templates = loader.hierarchy[loader_name].list_templates()
            self.assertEquals(expected_templates, actual_templates)

    def test_get_multi_hierarchy_loader(self):
        expected_multi_hierarchy = {
            'eurogamer_net': HierarchyLoader(
                OrderedDict((
                    ("eurogamer_net", FileSystemLoader(self.get_template_dir("eurogamer_net"))),
                    ("eurogamer", FileSystemLoader(self.get_template_dir("eurogamer"))),
                    ("core", FileSystemLoader(self.get_template_dir("core"))),
                ))
            ),
            'eurogamer_de': HierarchyLoader(
                OrderedDict((
                    ("eurogamer_de", FileSystemLoader(self.get_template_dir("eurogamer_de"))),
                    ("eurogamer", FileSystemLoader(self.get_template_dir("eurogamer"))),
                    ("core", FileSystemLoader(self.get_template_dir("core"))),
                ))
            ),
            'vg247_com': HierarchyLoader(
                OrderedDict((
                    ("vg247_com", FileSystemLoader(self.get_template_dir("vg247_com"))),
                    ("vg247", FileSystemLoader(self.get_template_dir("vg247"))),
                    ("core", FileSystemLoader(self.get_template_dir("core"))),
                ))
            ),
            'vg247_pl': HierarchyLoader(
                OrderedDict((
                    ("vg247_pl", FileSystemLoader(self.get_template_dir("vg247_pl"))),
                    ("vg247", FileSystemLoader(self.get_template_dir("vg247"))),
                    ("core", FileSystemLoader(self.get_template_dir("core"))),
                ))
            ),
        }
        loader = get_multi_hierarchy_loader(
            mock.Mock(),
            (
                ('eurogamer_net', (
                    ('eurogamer_net', self.get_template_dir('eurogamer_net')),
                    ('eurogamer', self.get_template_dir('eurogamer')),
                    ('core', self.get_template_dir('core')),
                )),
                ('eurogamer_de', (
                    ('eurogamer_de', self.get_template_dir('eurogamer_de')),
                    ('eurogamer', self.get_template_dir('eurogamer')),
                    ('core', self.get_template_dir('core')),
                )),
                ('vg247_com', (
                    ('vg247_com', self.get_template_dir('vg247_com')),
                    ('vg247', self.get_template_dir('vg247')),
                    ('core', self.get_template_dir('core')),
                )),
                ('vg247_pl', (
                    ('vg247_pl', self.get_template_dir('vg247_pl')),
                    ('vg247', self.get_template_dir('vg247')),
                    ('core', self.get_template_dir('core')),
                )),
            )
        )
        expected_hierarchy_chain = list(expected_multi_hierarchy.keys())
        expected_hierarchy_len = len(expected_hierarchy_chain)
        actual_hierarchy_chain = list(loader.hierarchies.keys())
        for i in range(expected_hierarchy_len):
            # Make sure the hierarchy is in the expected order
            loader_name = actual_hierarchy_chain[i]
            self.assertEquals(expected_hierarchy_chain[i], actual_hierarchy_chain[i])
            # Make sure the templates contained within the built loader is
            # identical to what we are expecting
            expected_templates = expected_multi_hierarchy[loader_name].list_templates()
            actual_templates = loader.hierarchies[loader_name].list_templates()
            self.assertEquals(expected_templates, actual_templates)

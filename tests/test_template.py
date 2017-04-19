import unittest

from jinja2.ext import Extension
from jinja2 import nodes

from gn_django.template.backend import Jinja2

class TestJinja2(unittest.TestCase):
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

from jinja2 import nodes, exceptions, runtime, environment
from jinja2.ext import Extension
from django.conf import settings as dj_settings

import re

class SpacelessExtension(Extension):
    """
    Removes whitespace between HTML tags at compile time, including tab and newline characters.
    It does not remove whitespace between jinja2 tags or variables. Neither does it remove whitespace between tags
    and their text content.
    Adapted from coffin:
        https://github.com/coffin/coffin/blob/master/coffin/template/defaulttags.py
    Usage:
        ``{% spaceless %}fooo bar baz{% endspaceless %}``
    """

    tags = set(['spaceless'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(['name:endspaceless'], drop_needle=True)
        return nodes.CallBlock(
            self.call_method('_strip_spaces', [], [], None, None),
            [], [], body,
        ).set_lineno(lineno)

    def _strip_spaces(self, caller=None):
        return re.sub(r'>\s+<', '><', caller().strip())

class IncludeWithExtension(Extension):
    """
    Includes a template with an explicitly declared context.
    Usage:
        ``{% include_with 'sometemplate.j2' foo='bar', hello=['world'] %}``
    """

    tags = set(['include_with'])

    def parse(self, parser):
        # First part will be 'include_with' tag, but also contains line number which
        # we use
        first = parser.parse_expression()

        # Second part is the template name
        template = parser.parse_expression()

        # Grab the context variables
        context = self._get_params(parser)
        call = self.call_method('_render', [template, context], lineno=first.lineno)

        return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

    def _render(self, template, context, caller):
        """
        Render the template with context variables

        Params:
            - `template` - The name of the template to render
            - `context` - The context to pass to the template
            - `caller` - Required by Jinja2

        Returns:
            - The parsed template
        """
        return self.environment.get_template(template).render(context)

    def _get_params(self, parser):
        """
        Parses the statement to collect the parameters given

        Returns:
            - `nodes.Dict` - A dictionary node containing instances of `nodes.Pair` representing
                the key/value pairs in the context
        """
        # Argument parsing adapted from https://github.com/coffin/coffin/blob/master/coffin/common.py#L164
        stream = parser.stream
        kwargs = []
        eval_ctx = nodes.EvalContext(self.environment)
        while not stream.current.test_any('block_end'):
            if kwargs:
                stream.expect('comma')
            if stream.current.test('name') and stream.look().test('assign'):
                key = nodes.Const(next(stream).value)
                stream.skip()
                value = parser.parse_expression()
                kwargs.append(nodes.Pair(key, value, lineno=key.lineno))
        if not kwargs:
            parser.fail('`include_with` tag must have parameters. Use `include` instead', lineno=stream.current.lineno)

        kwargs = nodes.Dict(kwargs)

        return kwargs

class CSSExtension(Extension):
    tags = set(['css'])

    def parse(self, parser):
        first = parser.parse_expression()
        name = parser.parse_expression()

        call = self.call_method('_render', [name], lineno=first.lineno)

        return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

    def _render(self, name, caller):
        debug_less = hasattr(dj_settings, 'DEBUG_LESS') and dj_settings.DEBUG_LESS
        ext = 'css'
        version = '?v={{ randint(minimum=0,maximum=99999) }}'
        append = ''
        if debug_less:
            less_compiler = ''
            if hasattr(dj_settings, 'CLIENT_LESS_COMPILER'):
                less_compiler = '<script src="%s"></script>' % dj_settings.CLIENT_LESS_COMPILER
            ext = 'less'
            version = ''
            append = """
<script>
    localStorage.clear();
    less = { env: "development" }
</script>
%s            """ % less_compiler

        template = '<link href="{{ static("%s/%s.%s") }}%s" rel="stylesheet" type="text/css" />%s' % (ext, name, ext, version, append)

        return self.environment.from_string(template).render()

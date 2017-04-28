from jinja2 import nodes, exceptions, runtime, environment
from jinja2.ext import Extension
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

    tags = set(['include_with'])

    def parse(self, parser):

        # First part will be 'include_with' tag, but also contains line number which
        # we use
        first = parser.parse_expression()

        # Second part is the template name
        template = parser.parse_expression()

        # Grab the context variables
        cvars = self._get_params(parser)

        ctx = nodes.ContextReference()
        call = self.call_method('_render', [template, cvars, ctx], lineno=first.lineno)

        return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

    def _render(self, template, cvars, ctx, caller):
        return self.environment.get_template(template).render(cvars)

    def _get_params(self, parser):
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

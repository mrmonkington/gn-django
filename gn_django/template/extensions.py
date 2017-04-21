from jinja2 import nodes, exceptions, runtime
from jinja2.ext import Extension
import copy

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
    valid_tags = [
        'comma',     # ','
        'assign',    # '='
        'colon',     # ':'
        'lbrace',    # '{'
        'rbrace',    # '}'
        'lparen',    # '('
        'rparen',    # ')'
        'lbracket',  # '['
        'rbracket',  # ']'
    ]

    def parse(self, parser):
        first = next(parser.stream)
        template = next(parser.stream).value
        cvars = self._get_context_vars(parser)
        node = nodes.Const(self.environment.get_template(template).render(cvars))
        return nodes.Output([node])

    def _get_context_vars(self, parser):
        current = None
        context = {}
        eval_ctx = nodes.EvalContext(self.environment)
        while not parser.stream.closed:
            try:
                old = parser.stream.current
                if old.type == 'block_end':
                    return context
                if parser.stream.skip_if('name'):
                    # Rewind and parse the name
                    parser.stream.current = old
                    token = parser.parse_expression()
                    current = token.name
                else:
                    try:
                        token = parser.parse_expression()
                        context[current] = token.as_const(eval_ctx)
                        current = None
                    except AttributeError:
                        pass
            except exceptions.TemplateSyntaxError as e:
                if not parser.stream.current.type in self.valid_tags:
                    raise e
                else:
                    parser.stream.skip()

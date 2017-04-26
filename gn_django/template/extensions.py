from jinja2 import nodes, exceptions, runtime, environment
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
        'data'
    ]

    def parse(self, parser):
        first = next(parser.stream)
        template = next(parser.stream).value
        cvars = self._get_context_vars(parser)
        print(cvars)
        node = nodes.Const(self.environment.get_template(template).render(cvars))
        return nodes.Output([node])

    def _get_context_vars(self, parser):
        # Argument parsing copied from https://github.com/coffin/coffin/blob/master/coffin/common.py#L164
        stream = parser.stream
        args = []
        kwargs = []
        eval_ctx = nodes.EvalContext(self.environment)
        c = nodes.ContextReference()
        while not stream.current.test_any('block_end'):
            stream.skip_if('comma')
            if stream.current.test('name') and stream.look().test('assign'):
                print('here')
                key = nodes.Const(next(stream).value)
                stream.skip()
                value = parser.parse_expression()
                kwargs.append(nodes.Pair(key, value, lineno=key.lineno))

        return kwargs


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
                    if current == None:
                        current = token.name
                    else:
                        # print('%s' % token)
                        context[current] = nodes.Const([self.call_method('_render', [token, nodes.ContextReference()])]).set_lineno(parser.stream.current.lineno).as_const()
                        # context[current] = self._render(token)
                        # context[current] = nodes.CallBlock([self.call_method('_render', [nodes.Name('msg', 'load')])], [], [], []).set_lineno(token.lineno)
                        current = None
                else:
                    try:
                        token = parser.parse_expression()
                        context[current] = token.as_const('load')
                        current = None
                    except AttributeError:
                        pass
            except exceptions.TemplateSyntaxError as e:
                if not parser.stream.current.type in self.valid_tags:
                    raise e
                else:
                    parser.stream.skip()
        return context

    def _render(self, node, context, caller):
        # print('%s' % node)

        return context[node.name]

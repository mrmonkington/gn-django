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

    def parse(self, parser):
        ctx_ref = nodes.ContextReference()
        ctx_ref['foo'] = 'bar'
        first = next(parser.stream)
        template = first.value
        lineno = first.lineno
        lineno = next(parser.stream).lineno
        node = nodes.Include(template, False, True, lineno=lineno)
        cvars = {'stuff': {'key': 'value'}}
        # cvars = self._get_context_vars(parser)
        context = runtime.Context(self.environment, {}, 'name', {})
        context.vars = cvars
        print(cvars)
        print(context)
        print(parser.stream)

        return nodes.CallBlock(node)
        # if parser.stream.current.test('name:ignore') and parser.stream.look().test('name:missing'):
        #     node.ignore_missing = True
        #     parser.stream.skip(2)
        # else:
        #     node.ignore_missing = False
        return parser.parse_import_context(node, True)

    def _get_context_vars(self, parser):
        current = None
        template = None
        context = {}
        eval_ctx = nodes.EvalContext(self.environment)
        try:
            for token in parser.stream:
                try:
                    t = parser.parse_expression()
                    if template == None and isinstance(t, nodes.Const):
                        template = t.value
                        lineno = t.lineno
                    elif current == None and isinstance(t, nodes.Name):
                        current = t.name
                    elif current:
                        context[current] = t.as_const(eval_ctx)
                        current = None
                except exceptions.TemplateSyntaxError as e:
                    break
        except exceptions.TemplateSyntaxError as e:
            pass

        return nodes.Include(template, False, True, lineno=lineno)
        return context


        # print('balls lightyear')
        # args = [parser.parse_expression()]
        #
        # if parser.stream.skip_if('comma'):
        #     exp = parser.parse_expression()
        #     args.append(exp)
        # elif parser.steam.skip_if('assign'):
        #     exp = parser.parse_expression()
        #     print(exp)
        # else:
        #     args.append(nodes.Const(None))
        #
        # print(parser.stream)
        # context = parser.parse_include()
        # print(context)

    def _include_with(self, caller):
        return caller()

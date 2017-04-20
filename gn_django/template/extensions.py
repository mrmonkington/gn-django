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
        first = next(parser.stream)
        # template = nodes.Const(next(parser.stream).value)
        template = next(parser.stream).value
        cvars = {'stuff': {'key': 'value'}}
        # cvars = self._get_context_vars(parser)
        node = nodes.Const(self.environment.get_template(template).render(cvars))
        print(node)
        return nodes.Output([node])


    # Future reference, WithExtension is defined im jinja2.ext
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
                except nodes.Impossible as e:
                    print('IMPOSSIBLE')
                    print(t)
                    continue
        except exceptions.TemplateSyntaxError as e:
            pass

        return context



    def _gninclude_with(self, include='', caller=None):
        print("HII")
        #print(include)
        return ''
        return parser.parse_import_context(include, '')

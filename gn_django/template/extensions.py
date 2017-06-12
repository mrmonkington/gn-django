from jinja2 import nodes, exceptions, runtime, environment
from jinja2.ext import Extension
from django.conf import settings as dj_settings
from django.core import exceptions

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

class StaticLinkExtension(Extension):
    """
    Extension for injecting ``link`` tags for stylesheets. This will inject the
    ``less`` version of the file if ``DEBUG_LESS`` is set and is set to ``True``,
    or if ``DEBUG_LESS`` is not set but ``DEBUG`` is set to True. Otherwise it
    will link to the ``css`` version.

    For this extension to work, LESS files and CSS files must be mapped identically
    within their directories.

    Supported tags:
        - ``{% css '[name]' %}`` - Link to a stylesheet in the assets directory.
                                    The '[name]' is the path to the file relative
                                    to the assets directory that contains files
                                    of that type, with no file extension e.g.
                                    'static/css/pages/article.css' would be 'pages/article'
        - ``{% compile_less %}`` - Render the script tags to link to a JavaScript
                                    LESS compiler for the client side if LESS is in
                                    debug mode. If not, it will output nothing.

    Configurations:
        - ``DEBUG_LESS``            - Link to LESS files if true, and CSS if false.
                                        Defaults to the value of ``DEBUG``
        - ``CLIENT_LESS_COMPILER``  - The URL of the client-side LESS compiler. If
                                        not set, an exception will be thrown when
                                        trying to use ``compile_less`` in debug mode
        - ``STATIC_FILE_MAP``       - A dictionary mapping file extensions to directories
                                        within the static directory. All file extensions
                                        will default to a directory matching it (e.g.
                                        CSS files will be assumed to be in a ``css``
                                        directory).

    """

    tags = set(['css', 'js', 'load_compilers'])

    def __init__(self, *args, **kwargs):
        self.debug_less = self._debug_less()

        return super(StaticLinkExtension, self).__init__(*args, **kwargs)

    def parse(self, parser):
        first = parser.parse_expression()
        if first.name == 'load_compilers':
            call = self.call_method('_load_compilers', lineno=first.lineno)
        else:
            name = parser.parse_expression()
            # Method to call follows pattern of tag name preceeded with underscore
            call = self.call_method('_%s' % first.name, [name], lineno=first.lineno)

        return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

    def _css(self, name, caller):
        """
        Render link tags for stylesheets. If ``self.debug_less`` is set to true
        this will be the ``less`` version of the file.

        Params:
            - `name` - The name of the file
            - `caller` - Required by Jinja
        """
        ext = 'css'
        if self.debug_less:
            ext = 'less'
        file_dir = self._get_file_dir(ext)

        template = '<link href="{{ static("%s/%s.%s") }}?v={{ randint(minimum=0,maximum=99999) }}" rel="stylesheet" type="text/%s" />' % (file_dir, name, ext, ext)

        return self.environment.from_string(template).render()

    def _js(self, name, caller):
        ext = 'js'
        file_dir = self._get_file_dir(ext)
        script_type = 'application/javascript'

        template = '<script href="{{ static("%s/%s.%s") }}" type="%s"></script>' % (file_dir, name, ext, script_type)
        print(template)
        return self.environment.from_string(template).render()

    def _load_compilers(self, caller):
        """
        If ``self.debug_less`` is true, inject a script to compile LESS in the front end.
        The URL for the LESS compiler is set as ``CLIENT_LESS_COMPILER`` in the settings
        file.

        Params:
            - `caller` - Required by Jinja
        """
        if not self.debug_less:
            return self.environment.from_string('').render()

        template = ''

        if hasattr(dj_settings, 'STATICLINK_CLIENT_COMPILERS'):
            for compiler in dj_settings.STATICLINK_CLIENT_COMPILERS:
                template = '%s\n<script src="%s"></script>' % (template, compiler)

        template = "%s\n<script>localStorage.clear();</script>" % template

        return self.environment.from_string(template).render()

    def _debug_less(self):
        if hasattr(dj_settings, 'DEBUG_LESS'):
            return dj_settings.DEBUG_LESS
        return dj_settings.DEBUG

    def _get_file_dir(self, ext):
        if hasattr(dj_settings, 'STATIC_FILE_MAP'):
            return dj_settings.STATIC_FILE_MAP.get(ext, ext)

        return ext

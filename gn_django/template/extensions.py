from jinja2 import nodes, exceptions, runtime, environment
from jinja2.ext import Extension
from django.conf import settings as dj_settings
from django.core import exceptions
from django.utils.safestring import mark_safe

import re, time, os

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
    Extension for linking to static assets within a template, with the ability to
    render uncompiled scripts (such as LESS) when in DEBUG mode.

    For usage, see https://gamer-network-gn-django.readthedocs-hosted.com/en/latest/jinja_templates/writing_jinja_templates.html#static-link-extension

    Supported tags:
        - ``{% css '[name]' %}``    - Link to a stylesheet in the assets directory.
        - ``{% js '[name]' %}``     - Link to a script in the assets directory.
        - ``{% load_compilers %}``  - Prepare front end compilation for preprocessors.
    """

    tags = set(['css', 'js', 'load_compilers'])

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
        Render link tags for stylesheets. If debug mode is enabled this will be
        the uncompiled version of the file.

        Params:
            - `name` - The name of the file
            - `caller` - Required by Jinja
        """
        ext = 'css'
        if self._is_debug(ext):
            ext = self._get_preprocessor(ext)
        file_dir = self._get_file_dir(ext)

        template = '<link href="{{ static("%s/%s.%s") }}?v=%s" rel="stylesheet" type="text/%s" />' % (file_dir, name, ext, self._get_version(), ext)

        return self.environment.from_string(template).render()

    def _js(self, name, caller):
        """
        Render script tags for JavaScript

        Params:
            - `name` - The name of the file
            - `caller` - Required by Jinja
        """
        ext = 'js'
        file_dir = self._get_file_dir(ext)
        script_type = 'application/javascript'
        template = '<script src="{{ static("%s/%s.%s") }}?v=%s" type="%s"></script>' % (file_dir, name, ext, self._get_version(), script_type)

        return self.environment.from_string(template).render()

    def _load_compilers(self, caller):
        """
        If debug mode is enabled, inject front end compilers.

        Params:
            - `caller` - Required by Jinja
        """

        debug = dj_settings.DEBUG
        template = ''

        if hasattr(dj_settings, 'STATICLINK_CLIENT_COMPILERS'):
            for ext in dj_settings.STATICLINK_CLIENT_COMPILERS:
                if self._is_debug(ext):
                    debug = True
                    compiler = dj_settings.STATICLINK_CLIENT_COMPILERS[ext]
                    template = '%s\n<script src="%s"></script>' % (template, compiler)

        if debug:
            template = "%s\n<script>localStorage.clear();</script>" % template

        return self.environment.from_string(template).render()

    def _is_debug(self, ext):
        """
        Check if debug mode is enabled for a file type.

        Params:
            - `ext` - The file extension to check the debug mode for
        """
        if hasattr(dj_settings, 'STATICLINK_DEBUG'):
            return dj_settings.STATICLINK_DEBUG.get(ext, dj_settings.DEBUG)
        return False

    def _get_file_dir(self, ext):
        """
        Get the directory of a file type within the main static directory. This
        can be configured in the `STATICLINK_FILE_MAP` setting. If it is not set,
        it will be assumed to be the file extension.

        Params:
            - `ext` - The file extension
        """
        if hasattr(dj_settings, 'STATICLINK_FILE_MAP'):
            return dj_settings.STATICLINK_FILE_MAP.get(ext, ext)

        return ext

    def _get_preprocessor(self, ext):
        """
        Get the preprocessor for that file type, e.g. 'less' for 'css'. This is
        configured in the `STATICLINK_PREPROCESSORS` setting and is required for
        debug mode.

        Params:
            - `ext` - The file extension to get the preprocessor for
        """
        preprocessor = dj_settings.STATICLINK_PREPROCESSORS.get(ext, False)
        if preprocessor:
            return preprocessor
        raise exceptions.ImproperlyConfigured('Cannot render `%s` in debug mode, set preprocessor (eg `less`) in STATICLINK_PREPROCESSORS config' % ext)

    def _get_version(self):
        """
        Get the version number to append to the static file URLs. This is defined
        in the `STATICLINK_VERSION` setting, and defaults to "latest".
        """
        if hasattr(dj_settings, 'STATICLINK_VERSION'):
            return dj_settings.STATICLINK_VERSION
        return "latest"

class IncludeRawExtension(Extension):
    """
    Extension for outputting the contents of a static file without parsing it
    (useful for CSS).

    Usage:
        ``{% include_raw 'path/to/file.css' %}``

    Params:
        - `path/to/file.css` - Relative path to the file within a directory
           defined in the `STATICFILES_DIRS` setting.
    """

    tags = set(['include_raw'])

    def parse(self, parser):
        first = parser.parse_expression()
        path = parser.parse_expression()
        call = self.call_method('_get_file', [path], lineno=first.lineno)
        return nodes.CallBlock(call, [], [], [], lineno=first.lineno)

    def _get_file(self, path, caller):
        """
        Check if a file exists an the specified path, and if so then open it and
        render the contents.

        Params:
            - `path` - The path to the file
            - `caller` - Required by Jinja
        """
        output = ''

        if hasattr(dj_settings, 'STATICFILES_DIRS'):
            for static_dir in dj_settings.STATICFILES_DIRS:
                fp = os.path.join(static_dir, path)
                if os.path.isfile(fp):
                    f = open(fp, 'r')
                    output = f.read()
                    f.close()
                    break

        return output

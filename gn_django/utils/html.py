import html
import re


def htmlify_content(content):
    """
    Replace URLs with links and new lines with ``<br />`` tags, and HTML escape everything else.
    To output in templates, you will need to use the ``safe`` filter.
    """
    url_pattern = re.compile(r'(https?)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
    content = html.escape(content)
    content = re.sub(
        url_pattern,
        lambda c: '<a href="%s" target="_blank">%s</a>' % (c.group(0),c.group(0)),
        content
    )
    return '<br />'.join(content.split('\n'))

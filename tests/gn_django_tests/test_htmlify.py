from django.test import TestCase

from gn_django.utils import htmlify_content

class TestHtmlifyContent(TestCase):
    def test_url_parse(self):
        content = "http://example.com"
        self.assertEqual(htmlify_content(content), '<a href="http://example.com" target="_blank">http://example.com</a>')

    def test_nl_parse(self):
        content = """hello
world"""
        self.assertEqual(htmlify_content(content), "hello<br />world")

    def test_char_escape(self):
        content = "<script>website.hack()</script>"
        self.assertEqual(htmlify_content(content), "&lt;script&gt;website.hack()&lt;/script&gt;")

    def test_content_block_parse(self):
        content = """you can find my work at http://mysuperwebsite.net
but also I'm a <script>echo "1337 h4xxx0r"</script> so that's something
to bear in mind"""
        expected = "you can find my work at <a href=\"http://mysuperwebsite.net\" target=\"_blank\">http://mysuperwebsite.net</a><br />but also I&#x27;m a &lt;script&gt;echo &quot;1337 h4xxx0r&quot;&lt;/script&gt; so that&#x27;s something<br />to bear in mind"
        self.assertEqual(htmlify_content(content), expected)

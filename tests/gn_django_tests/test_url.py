import unittest

from gn_django.url import utils

class TestUrlUtils(unittest.TestCase):
    """
    Tests for URL util functions
    """

    def test_strip_protocol_http(self):
        url = 'http://www.example.com'
        stripped = utils.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_https(self):
        url = 'https://www.example.com'
        stripped = utils.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_relative(self):
        url = '//www.example.com'
        stripped = utils.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_none(self):
        url = 'www.example.com'
        stripped = utils.strip_protocol(url)
        self.assertEqual('www.example.com', stripped)

    def test_add_params_to_url_with_no_params(self):
        url = "/a/b/c"
        url_with_params = utils.add_params_to_url(url, foo="bar", baz="woo")
        self.assertEqual("/a/b/c", url_with_params.split('?')[0])
        self.assertTrue("foo=bar" in url_with_params)
        self.assertTrue("baz=woo" in url_with_params)

    def test_add_params_to_url_with_params_already(self):
        url = "/a/b/c?lol=ayyy"
        url_with_params = utils.add_params_to_url(url, foo="bar", baz="woo")
        self.assertEqual("/a/b/c", url_with_params.split('?')[0])
        self.assertTrue("foo=bar" in url_with_params)
        self.assertTrue("baz=woo" in url_with_params)
        self.assertTrue("lol=ayyy" in url_with_params)

    def test_add_params_to_url_param_values_unencoded(self):
        url = "/a/b/c"
        url_with_params = utils.add_params_to_url(url, foo="bar helloo", baz="woo||yo")
        self.assertEqual("/a/b/c", url_with_params.split('?')[0])
        self.assertTrue("foo=bar+helloo" in url_with_params)
        self.assertTrue("baz=woo%7C%7Cyo" in url_with_params)

    def test_add_path_to_url(self):
        url = "/path/to"
        to_add = "a/resource"
        full_url = utils.add_path_to_url(url, to_add)
        self.assertEqual("/path/to/a/resource", full_url)

    def test_add_path_to_url_trailing_slash(self):
        url = "/path/to/"
        to_add = "a/resource"
        full_url = utils.add_path_to_url(url, to_add)
        self.assertEqual("/path/to/a/resource", full_url)

    def test_add_path_to_url_trailing_and_leading_slash(self):
        url = "/path/to/"
        to_add = "/a/resource"
        full_url = utils.add_path_to_url(url, to_add)
        self.assertEqual("/path/to/a/resource", full_url)

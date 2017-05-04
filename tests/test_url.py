import unittest

from gn_django.url import helpers

class TestUrlHelpers(unittest.TestCase):
    """
    Tests for URL helper functions
    """

    def test_strip_protocol_http(self):
        url = 'http://www.example.com'
        stripped = helpers.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_https(self):
        url = 'https://www.example.com'
        stripped = helpers.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_relative(self):
        url = '//www.example.com'
        stripped = helpers.strip_protocol(url)
        self.assertEqual('//www.example.com', stripped)

    def test_strip_protocol_none(self):
        url = 'www.example.com'
        stripped = helpers.strip_protocol(url)
        self.assertEqual('www.example.com', stripped)

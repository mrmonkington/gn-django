import unittest

from gn_django import utils

class TestFormUtils(unittest.TestCase):
    """
    Tests for gn-django general util functions
    """

    def test_convert_camelcase_to_slugified(self):
        camel = "ACamelCaseString"
        slugified = utils.convert_camelcase_to_slugified(camel)
        self.assertEqual(slugified, "a-camel-case-string")

    def test_convert_camelcase_to_slugified_already_slugified(self):
        camel = "a-camel-case-string"
        slugified = utils.convert_camelcase_to_slugified(camel)
        self.assertEqual(slugified, "a-camel-case-string")

import unittest

from gn_django.utils import camelize


class TestCamelize(unittest.TestCase):
    def test_camelize_from_snek(self):
        self.assertEqual('IAmACamel', camelize('i_am_a_camel'))

    def test_camelize_from_spaces(self):
        self.assertEqual('IAmACamel', camelize('I am a camel'))

    def test_camelize_one_word(self):
        self.assertEqual('Camel', camelize('camel'))

    def test_camelize_special_chars(self):
        self.assertEqual('IAmACamel', camelize('i_-£$%"AM(((a+=-.cAmEl'))

    def test_camelize_with_numbers(self):
        self.assertEqual('IAmCamel100', camelize('i_am_camel_100'))

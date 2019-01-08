import json
from django.test import TestCase
from gn_django.models import LazyAttributes, LazyAttributesMixin

class MockAttributesParent(LazyAttributesMixin):
    attributes = {
        'a': 'aa',
        'b': 'bb',
        'c': 'cc',
        'd': 'dd',
    }

parent = MockAttributesParent()

class MockAttributesChild(LazyAttributesMixin):
    parent = parent
    override_attributes = {
        'b': 'BEE',
        'c': 'SEA'
    }

    def __init__(self):
        self._setup_attributes()

child = MockAttributesChild()

class MockAttributesGrandchild(LazyAttributesMixin):
    parent = child
    override_attributes = {
        'c': 'si',
        'd': 'di', 
        'e': 'ee',
    }

    def __init__(self):
        self._setup_attributes()

grandchild = MockAttributesGrandchild()

class TestLazyAttributes(TestCase):
    def setUp(self):
        self.parent = parent
        self.child = child
        self.grandchild = grandchild

    def test_get_attributes(self):
        self.assertEqual(self.parent.attributes['a'], 'aa')
        self.assertEqual(self.child.attributes['a'], 'aa')
        self.assertEqual(self.grandchild.attributes['a'], 'aa')

        self.assertEqual(self.parent.attributes['b'], 'bb')
        self.assertEqual(self.child.attributes['b'], 'BEE')
        self.assertEqual(self.grandchild.attributes['b'], 'BEE')

        self.assertEqual(self.parent.attributes['c'], 'cc')
        self.assertEqual(self.child.attributes['c'], 'SEA')
        self.assertEqual(self.grandchild.attributes['c'], 'si')

        self.assertEqual(self.parent.attributes['d'], 'dd')
        self.assertEqual(self.child.attributes['d'], 'dd')
        self.assertEqual(self.grandchild.attributes['d'], 'di')

        self.assertEqual(self.grandchild.attributes['e'], 'ee')

    def test_get_all_attributes(self):
        expected = {
            'a': 'aa',
            'b': 'BEE',
            'c': 'si',
            'd': 'di',
            'e': 'ee',
        }
        self.assertEqual(self.grandchild.get_all_attributes(), expected)
        self.assertEqual(json.loads(self.grandchild.get_all_attributes(as_json=True)), expected)

    def test_get_inherited_attributes(self):
        expected = {
            'a': 'aa',
            'b': 'BEE',
        }
        self.assertEqual(self.grandchild.get_inherited_attributes(), expected)
        self.assertEqual(json.loads(self.grandchild.get_inherited_attributes(as_json=True)), expected)
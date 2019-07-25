from django.test import TestCase

from gn_django.utils import compare_dicts, flatten_dict


class TestCompareDicts(TestCase):
    """
    Test the compare_dicts utility function.

    Note: most tests on this are repeated twice to assert the commutative
    property of this function, i.e. comparing A to B should be equivalent to
    comparing B to A.
    """
    def test_compare_equal(self):
        """
        Test comparison for dicts which are equal.
        """
        # Trivial case
        self.assertEqual({}, compare_dicts({}, {}))
        # Two identical dictionaries
        self.assertEqual({
            'foo': False,
            'baz': [False],
            'one': {'two': False},
        }, compare_dicts(
            {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}},
            {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}},
        ))

    def test_compare_equal_disordered(self):
        """
        Test comparison for dicts which are equal but in different orders.
        """
        self.assertEqual({
            'foo': False,
            'baz': [False],
            'one': {'two': False},
        }, compare_dicts(
            {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}},
            {'one': {'two': 'three'}, 'foo': 'bar', 'baz': ['quuz']},
        ))
        # Assert commutative
        self.assertEqual({
            'foo': False,
            'baz': [False],
            'one': {'two': False},
        }, compare_dicts(
            {'one': {'two': 'three'}, 'foo': 'bar', 'baz': ['quuz']},
            {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}},
        ))

    def test_compare_to_empty(self):
        """
        Test comparison for dicts where one of the arguments is empty.
        """
        # Test comparing to an empty dict
        self.assertEqual({
            'foo': True,
            'baz': True,
            'one': True,
        }, compare_dicts({'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}}, {}))
        # Assert commutative
        self.assertEqual({
            'foo': True,
            'baz': True,
            'one': True,
        }, compare_dicts({}, {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}}))

        # Test comparing when a sub-element is an empty dict
        self.assertEqual({
            'foo': False,
            'baz': [False],
            'one': {'two': True},
        }, compare_dicts(
            {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}},
            {'foo': 'bar', 'baz': ['quuz'], 'one': {}},
        ))
        # Assert commutative
        self.assertEqual({
            'foo': False,
            'baz': [False],
            'one': {'two': True},
        }, compare_dicts(
            {'foo': 'bar', 'baz': ['quuz'], 'one': {}},
            {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}},
        ))

    def test_compare_regular(self):
        """
        Test comparison with regular dictionary data.
        """
        # Test comaring similar objects
        self.assertEqual({
            'foo': False,
            'baz': [False, True],
            'one': {'two': True},
        }, compare_dicts(
            {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}},
            {'foo': 'bar', 'baz': ['quuz', 'zu'], 'one': {'two': 4}},
        ))
        # Assert commutative
        self.assertEqual({
            'foo': False,
            'baz': [False, True],
            'one': {'two': True},
        }, compare_dicts(
            {'foo': 'bar', 'baz': ['quuz', 'zu'], 'one': {'two': 4}},
            {'foo': 'bar', 'baz': ['quuz'], 'one': {'two': 'three'}},
        ))
        # Test comparing entirely different objects
        self.assertEqual({
            'foo': True,
            'baz': True,
            'marco': True,
            'polo': True,
        }, compare_dicts(
            {'foo': 'bar', 'marco': 'polo'},
            {'baz': 'quux', 'polo': 'marco'},
        ))
        # Assert commutative
        self.assertEqual({
            'foo': True,
            'baz': True,
            'marco': True,
            'polo': True,
        }, compare_dicts(
            {'baz': 'quux', 'polo': 'marco'},
            {'foo': 'bar', 'marco': 'polo'},
        ))


class TestFlattenDict(TestCase):
    def test_flatten_dict_trivial(self):
        """
        Test flatten_dict() on trivial values
        """
        self.assertEqual({}, flatten_dict({}))
        self.assertEqual(
            {'foo': 'bar', 'bar__baz': 'quux'},
            flatten_dict({'foo': 'bar', 'bar__baz': 'quux'}),
        )

    def test_flatten_dict(self):
        self.assertEqual(
            {
                'foo__bar__0': 'baz',
                'foo__bar__1': 'bazza',
                'foo__bar__2': 1456,
                'foo__quux': True,
                'foo__foo__bar': 'bar',
                'bar': 'quux',
            },
            flatten_dict({
                'foo': {
                    'bar': [
                        'baz',
                        'bazza',
                        1456,
                    ],
                    'quux': True,
                    'foo': {
                        'bar': 'bar',
                    },
                },
                'bar': 'quux',
            }),
        )

    def test_flatten_dict_with_prefix(self):
        self.assertEqual(
            {
                'prefix__foo__bar__0': 'baz',
                'prefix__foo__bar__1': 'bazza',
                'prefix__foo__bar__2': 1456,
                'prefix__foo__quux': True,
                'prefix__foo__foo__bar': 'bar',
                'prefix__bar': 'quux',
            },
            flatten_dict({
                'foo': {
                    'bar': [
                        'baz',
                        'bazza',
                        1456,
                    ],
                    'quux': True,
                    'foo': {
                        'bar': 'bar',
                    },
                },
                'bar': 'quux',
            }, prefix='prefix__'),
        )

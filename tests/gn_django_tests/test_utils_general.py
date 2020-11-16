from unittest.mock import patch

from django.db.models import QuerySet
from django.test import TestCase

from gn_django.utils import all_subclasses, count


class TestAllSubclasses(TestCase):
    def test_gets_subclass_of_direct_parent_class(self):
        """
        Gets a class if it is a direct child of the parent class.
        """
        class Parent:
            pass

        class Child(Parent):
            pass

        subclasses = list(all_subclasses(Parent))
        subclass = subclasses[0]

        self.assertEqual(len(subclasses), 1)
        self.assertEqual(subclass.__name__, 'Child')

    def test_gets_subclass_of_indirect_parent_class(self):
        """
        Gets a class if it is an indirect child of the parent class.
        """
        class Parent:
            pass

        class Child(Parent):
            pass

        class GrandChild(Child):
            pass

        subclasses = list(all_subclasses(Parent))
        self.assertEqual(len(subclasses), 2)
        self.assertTrue('Child' in [sc.__name__ for sc in subclasses])
        self.assertTrue('GrandChild' in [sc.__name__ for sc in subclasses])

    def test_does_not_get_subclass_of_different_parent_class(self):
        """
        Gets a class if it is an indirect child of the parent class.
        """
        class Parent:
            pass

        class Other:
            pass

        class Child(Other):
            pass

        subclasses = list(all_subclasses(Parent))
        self.assertEqual(len(subclasses), 0)


class TestCount(TestCase):
    @patch('django.db.models.QuerySet.count')
    def test_count_queryset(self, qs_count):
        qs_count.return_value = 7
        qs = QuerySet()
        self.assertEqual(7, count(qs))

    def test_count_iterable(self):
        self.assertEqual(7, count([0, 1, 2, 3, 4, 5, 6]))

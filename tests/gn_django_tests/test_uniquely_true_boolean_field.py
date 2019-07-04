from django.test import TestCase

from gn_django.fields import UniquelyTrueBooleanField

from core.models import TestUniquelyTrueBooleanModel

class TestUniquelyTrueBooleanField(TestCase):

    def test_cannot_add_a_second_instance_with_true(self):
        """
        A ``ValueError`` will be raised if an attempt is made to save an
        instance with ``unique_field=True`` when one already exists in the db.
        """
        TestUniquelyTrueBooleanModel.objects.create(
            is_the_chosen_one=True
        )
        with self.assertRaises(ValueError):
            TestUniquelyTrueBooleanModel.objects.create(
                is_the_chosen_one=True
            )

    def test_setting_false_raises_exception(self):
        """
        When a value of ``False`` is given, a ``ValueError`` is raised.
        """
        with self.assertRaises(ValueError):
            TestUniquelyTrueBooleanModel.objects.create(
                is_the_chosen_one=False
            )

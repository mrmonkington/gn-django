from django.test import TestCase

from gn_django.utils import qs_to_choices


class TestQSToChoices(TestCase):

    class TestClass:

        pk = 1
        name = 'Some name'
        slug = 'some-slug'

        def __str__(self):
            return 'Some string :)'

    def test_defaults(self):
        instance = self.TestClass()
        qs = [instance]
        choices = qs_to_choices(qs)
        self.assertEqual(choices[0][0], instance.pk)
        self.assertEqual(choices[0][1], str(instance))

    def test_specify_val_and_label(self):
        instance = self.TestClass()
        qs = [instance]
        choices = qs_to_choices(qs, 'slug', 'name')
        self.assertEqual(choices[0][0], instance.slug)
        self.assertEqual(choices[0][1], instance.name)

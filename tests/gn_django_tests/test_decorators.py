from django.test import TestCase

from gn_django.decorators import classproperty

class MyClass:
    
    @classproperty
    def foo(cls):
        return "bar"

class TestClassProperty(TestCase):

    def test_classproperty(self):
        self.assertEqual(MyClass.foo, "bar")

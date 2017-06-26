import unittest

from django import forms

from gn_django.form import utils

class SampleBlogForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.CharField(max_length=50)
    author_email = forms.EmailField(max_length=50, required=False)
    publication_date = forms.DateTimeField()
    

class TestFormUtils(unittest.TestCase):
    """
    Tests for form util functions
    """

    def test_get_form_error_dict_form_without_error(self):
        form = SampleBlogForm({'title': "My blog", "author": "Brendan", "publication_date": "2017-06-01 12:00:00"})
        self.assertTrue(form.is_valid())
        self.assertEquals(utils.get_form_error_dict(form), {})

    def test_get_form_error_dict_form_with_one_error(self):
        form = SampleBlogForm({"author": "Brendan", "publication_date": "2017-06-01 12:00:00"})
        self.assertFalse(form.is_valid())
        self.assertEquals(utils.get_form_error_dict(form), {'title': 'This field is required'})

    def test_get_form_error_dict_form_with_multiple_errors(self):
        form = SampleBlogForm({"author": "Brendan"*20, "publication_date": "2017-06-01 12:00:00"})
        self.assertFalse(form.is_valid())
        self.assertEquals(utils.get_form_error_dict(form), {'title': 'This field is required', 'author': 'Ensure this value has at most 50 characters (it has 140)'})

    def test_get_form_error_dict_form_with_multiple_errors_single_field(self):
        form = SampleBlogForm({'title': "My blog", "author": "Brendan", "publication_date": "2017-06-01 12:00:00", 'author_email': ("brendan"*50) + "smithatgmail.com"})
        self.assertFalse(form.is_valid())
        self.assertEquals(utils.get_form_error_dict(form), {'author_email': 'Enter a valid email address, Ensure this value has at most 50 characters (it has 366)'})

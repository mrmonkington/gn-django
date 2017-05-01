from unittest import mock

from django.test import TestCase, override_settings
from django.views.generic.base import View
from django.conf import settings

from gn_django.view import view_registry

class TestViewRegistry(TestCase):

    def test_register(self):
        """
        Test that views can be registered.
        """
        view = mock.Mock()
        view_registry.register('wibble:Article', view)
        # Registry populated with view
        self.assertEquals(view_registry._registry['wibble']['Article'], view.as_view())
        # Exception raised when the view label is malformed 
        self.assertRaises(Exception, view_registry.register, ('wibbleArticle', view))

    def test_register_app_views(self):
        """
        Test that a module of views can be registered under a particular
        application namespace.
        """
        # Create a mocked views.py module
        views_module = mock.Mock()
        views_module.__name__ = 'fooob.views'
        views = []
        # Create 5 mocked views within our module
        for i in range(5):
            view_func = mock.Mock()
            class AView(View):
                
                def as_view():
                    return view_func
            view = AView
            view_name = 'View%s' % i
            view.__name__ = view_name
            view.__module__ = views_module.__name__
            views.append(view)
            setattr(views_module, view_name, view)
        # Register our module in the registry
        view_registry.register_app_views('fooob', views_module)
        # Test that our views are present in the registry
        for view in views:
            self.assertEquals(view_registry._registry['fooob'][view.__name__], view.as_view())

    def test_get(self):
        """
        Test that views can be retrieved from the registry successfully.
        """
        # Prime the registry with some mocked views
        views = [(mock.Mock(), 'View%s' % i) for i in range(5)]
        # We need to patch the existing _registry for the duration of this test
        with mock.patch.dict(view_registry._registry, {}):
            view_registry._registry['main'] = {}
            for view_func, view_name in views:
                view_registry._registry['main'][view_name] = view_func
            # Assert that the views can be retrieved with `get`
            for view_func, view_name in views:
                view_wrapper = view_registry.get('main:%s' % view_name)
                called_view = view_wrapper()
                self.assertEquals(view_func(), called_view)
            

    def test_view_registry_in_project(self):
        """
        Test that the view registry is working in a running django
        environment.
        """
        # The archive view is registered on the `core` app only
        archive_response = self.client.get('/archive')
        self.assertTrue("Archive from app: core" in archive_response.content.decode('utf-8'))
        # The article view is registered on the `content` app only
        article_response = self.client.get('/article')
        self.assertTrue("Article from app: content" in article_response.content.decode('utf-8'))
        # The about view is registered on the `core` app and then overidden
        # in the `content` app
        about_response = self.client.get('/about')
        self.assertTrue("About from app: content" in about_response.content.decode('utf-8'))

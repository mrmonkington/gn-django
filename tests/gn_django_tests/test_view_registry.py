from unittest import mock

from django.test import TestCase, override_settings
from django.views.generic.base import View
from django.conf import settings

from gn_django.app import view_registry
from gn_django.app import GNAppConfig

class TestViewRegistry(TestCase):

    def test_initialise_view_registry(self):
        """
        Test the initialise_view_registry function successfully builds a
        view registry from a mocked apps config.
        """
        first_app = mock.Mock(spec=GNAppConfig)
        first_app.name = "core"
        first_app.views = {'core:Home': mock.Mock(spec=View)}
        second_app = mock.Mock(spec=GNAppConfig)
        second_app.name = "content"
        second_app.views = {'core:Home': mock.Mock(spec=View), 'content:Article': mock.Mock(spec=View)}
        mocked_app_config = [
            first_app,
            second_app,
        ]
        expected_registry = {
            'core': {
                'Home': second_app.views['core:Home'].as_view(),
            },
            'content': {
                'Article': second_app.views['content:Article'].as_view(),
            }
        }
        with mock.patch.dict(view_registry._registry, {}, clear=True):
            with mock.patch("django.apps.apps.get_app_configs") as mocked_get_app_configs:
                mocked_get_app_configs.return_value = mocked_app_config
                view_registry.initialise_view_registry()
                self.assertEquals(view_registry._registry, expected_registry)

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

    def test_get_wraps(self):
        """
        Test that views are wrapped, i.e. properties on the original view
        function still exist on the registry version.
        """
        view_func = mock.Mock()
        setattr(view_func, 'some_arbitary_attr', 'some_value')
        with mock.patch.dict(view_registry._registry, {
            'main': {'TestView': view_func},
        }):
            view_wrapper = view_registry.get('main:TestView')
            self.assertEqual(
                'some_value',
                getattr(view_wrapper, 'some_arbitary_attr'),
            )

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


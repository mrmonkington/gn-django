from django.test import TestCase, override_settings
from django.conf import settings

from gn_django.site import get_current_site, get_namespace_for_site, set_current_site, clear_current_site

site_settings = {
    'ALLOWED_HOSTS': ['*'], 
    'MIDDLEWARE': [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'gn_django.site.middleware.SiteFromDomainMiddleware',
    ],
    'SITE_DOMAINS': {
        "127.0.0.1": "eurogamer.net",
        "eurogamer.net.local": "eurogamer.net",
        "eurogamer.de.local": "eurogamer.de",
        "vg247.com.local": "vg247.com",
        "vg247.pl.local": "vg247.pl",
    },
    'SITE_NAMESPACES': {
        "eurogamer.net": "eurogamer_net",
        "eurogamer.de": "eurogamer_de",
        "vg247.com": "vg247_com",
        "vg247.pl": "vg247_pl",
    }
}

@override_settings(**site_settings)
class TestSiteFromDomainMiddleware(TestCase):

    def test_middleware_sets_site(self):
        """
        Functional test that the SiteFromDomainMiddleware is working correctly
        to set the current site.
        """
        test_cases = [
            ("eurogamer.net.local", "eurogamer.net",),
            ("eurogamer.de.local", "eurogamer.de",),
            ("vg247.pl.local", "vg247.pl",),
            ("vg247.com.local", "vg247.com",),
        ]
        for host, expected_site in test_cases:
            response = self.client.get('/site', SERVER_NAME=host)
            self.assertTrue(("Site: %s" % expected_site) in response.content.decode('utf-8'))

    def test_middleware_sets_site_namespace(self):
        """
        Functional test that the SiteFromDomainMiddleware is working correctly to 
        set the current namespace.
        """
        test_cases = [
            ("eurogamer.net.local", "eurogamer_net",),
            ("eurogamer.de.local", "eurogamer_de",),
            ("vg247.pl.local", "vg247_pl",),
            ("vg247.com.local", "vg247_com",),
        ]
        for host, expected_namespace in test_cases:
            response = self.client.get('/site', SERVER_NAME=host)
            self.assertTrue(("Namespace: %s" % expected_namespace) in response.content.decode('utf-8'))


@override_settings(**site_settings)
class TestSiteFunctions(TestCase):

    def tearDown(self):
        clear_current_site()

    def test_get_current_site(self):
        """
        Test get_current_site function.
        """
        self.assertEquals(get_current_site(), None)
        set_current_site('eurogamer.net')
        self.assertEquals(get_current_site(), 'eurogamer.net')

    def test_set_current_site(self):
        """
        Test set_current_site function.
        """
        self.assertEquals(get_current_site(), None)
        set_current_site('eurogamer.net')
        self.assertEquals(get_current_site(), 'eurogamer.net')
        set_current_site('eurogamer.de')
        self.assertEquals(get_current_site(), 'eurogamer.de')

    def test_clear_current_site(self):
        """
        Test clear_current_site function.
        """
        self.assertEquals(get_current_site(), None)
        set_current_site('eurogamer.net')
        self.assertEquals(get_current_site(), 'eurogamer.net')
        clear_current_site()
        self.assertEquals(get_current_site(), None)

    def test_get_namespace_for_site(self):
        """
        Test get_namespace_for_site function.
        """
        self.assertEquals(get_namespace_for_site(), None)
        set_current_site('eurogamer.net')
        self.assertEquals(get_namespace_for_site(), 'eurogamer_net')
    def test_get_namespace_for_site_no_setting(self):
        """
        Test get_namespace_for_site function when SITE_NAMESPACES
        setting is not set.
        """
        deleted_setting = settings.SITE_NAMESPACES
        del settings.SITE_NAMESPACES
        self.assertRaises(Exception, get_namespace_for_site)
        settings.SITE_NAMESPACES = deleted_setting

    def test_get_namespace_for_site_unknown_site(self):
        """
        Test get_namespace_for_site function when SITE_NAMESPACES
        does not contain the domain that has been set.
        """
        set_current_site('foobar.net')
        self.assertRaises(KeyError, get_namespace_for_site)

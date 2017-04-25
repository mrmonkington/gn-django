from threading import local

from django.test import TestCase, override_settings
from django.conf import settings

from gn_django.site_domain import get_current_site_domain, get_namespace_for_site_domain, set_current_site_domain, clear_current_site_domain

site_domain_settings = {
    'ALLOWED_HOSTS': ['*'], 
    'MIDDLEWARE': [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'gn_django.site_domain.middleware.SiteDomainMiddleware',
    ],
    'SITE_DOMAIN_MAPPER': {
        "127.0.0.1": "eurogamer.net",
        "eurogamer.net.local": "eurogamer.net",
        "eurogamer.de.local": "eurogamer.de",
        "vg247.com.local": "vg247.com",
        "vg247.pl.local": "vg247.pl",
    },
    'SITE_DOMAIN_NAMESPACE_MAPPER': {
        "eurogamer.net": "eurogamer_net",
        "eurogamer.de": "eurogamer_de",
        "vg247.com": "vg247_com",
        "vg247.pl": "vg247_pl",
    }
}

@override_settings(**site_domain_settings)
class TestSiteDomainMiddleware(TestCase):

    def test_middleware_sets_site_domain(self):
        """
        Functional test that the SiteDomainMiddleware is working correctly
        to set the current site domain.
        """
        test_cases = [
            ("eurogamer.net.local", "eurogamer.net",),
            ("eurogamer.de.local", "eurogamer.de",),
            ("vg247.pl.local", "vg247.pl",),
            ("vg247.com.local", "vg247.com",),
        ]
        for host, expected_domain in test_cases:
            response = self.client.get('/domain', SERVER_NAME=host)
            self.assertTrue(("Domain: %s" % expected_domain) in response.content.decode('utf-8'))

    def test_middleware_sets_site_namespace(self):
        """
        Functional test that the SiteDomainMiddleware is working correctly to 
        set the current namespace.
        """
        test_cases = [
            ("eurogamer.net.local", "eurogamer_net",),
            ("eurogamer.de.local", "eurogamer_de",),
            ("vg247.pl.local", "vg247_pl",),
            ("vg247.com.local", "vg247_com",),
        ]
        for host, expected_namespace in test_cases:
            response = self.client.get('/domain', SERVER_NAME=host)
            self.assertTrue(("Namespace: %s" % expected_namespace) in response.content.decode('utf-8'))


@override_settings(**site_domain_settings)
class TestSiteDomainFunctions(TestCase):

    def tearDown(self):
        clear_current_site_domain()

    def test_get_current_site_domain(self):
        """
        Test get_current_site_domain function.
        """
        self.assertEquals(get_current_site_domain(), None)
        set_current_site_domain('eurogamer.net')
        self.assertEquals(get_current_site_domain(), 'eurogamer.net')

    def test_set_current_site_domain(self):
        """
        Test set_current_site_domain function.
        """
        self.assertEquals(get_current_site_domain(), None)
        set_current_site_domain('eurogamer.net')
        self.assertEquals(get_current_site_domain(), 'eurogamer.net')
        set_current_site_domain('eurogamer.de')
        self.assertEquals(get_current_site_domain(), 'eurogamer.de')

    def test_clear_current_site_domain(self):
        """
        Test clear_current_site_domain function.
        """
        self.assertEquals(get_current_site_domain(), None)
        set_current_site_domain('eurogamer.net')
        self.assertEquals(get_current_site_domain(), 'eurogamer.net')
        clear_current_site_domain()
        self.assertEquals(get_current_site_domain(), None)

    def test_get_namespace_for_site_domain(self):
        """
        Test get_namespace_for_site_domain function.
        """
        self.assertEquals(get_namespace_for_site_domain(), None)
        set_current_site_domain('eurogamer.net')
        self.assertEquals(get_namespace_for_site_domain(), 'eurogamer_net')
    def test_get_namespace_for_site_domain_no_setting(self):
        """
        Test get_namespace_for_site_domain function when SITE_DOMAIN_NAMESPACE_MAPPER
        setting is not set.
        """
        deleted_setting = settings.SITE_DOMAIN_NAMESPACE_MAPPER
        del settings.SITE_DOMAIN_NAMESPACE_MAPPER
        self.assertRaises(Exception, get_namespace_for_site_domain)
        settings.SITE_DOMAIN_NAMESPACE_MAPPER = deleted_setting

    def test_get_namespace_for_site_domain_unknown_domain(self):
        """
        Test get_namespace_for_site_domain function when SITE_DOMAIN_NAMESPACE_MAPPER
        does not contain the domain that has been set.
        """
        set_current_site_domain('foobar.net')
        self.assertRaises(KeyError, get_namespace_for_site_domain)

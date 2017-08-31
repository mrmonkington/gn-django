import unittest, time
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .selenium import GNRemote, browser_manager

RESOLUTIONS = {
    'desktop': '1920x1080',
    'portable_portrait': '1024x768',
    'portable_landscape': '768x1024',
    'mobile_large': '411x731',
    'mobile_small': '320x568',
}

@unittest.skipUnless(hasattr(settings, 'SELENIUM_RUN_TESTS') and settings.SELENIUM_RUN_TESTS, "Selenium tests not requested")
class AcceptanceTestCase(StaticLiveServerTestCase):
    """
    """

    host = settings.SELENIUM_APP_HOST
    browser_name = 'chrome'
    resolution = RESOLUTIONS['desktop']
    element_scroll_behavior = 'bottom'

    @classmethod
    def setUpClass(cls):
        capabilities = DesiredCapabilities.CHROME.copy()
        if (cls.browser_name == 'firefox'):
            capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities['elementScrollBehavior'] = cls.element_scroll_behavior
        capabilities['screenResolution'] = cls.resolution
        cls.browser = browser_manager.get_browser(capabilities)
        return super().setUpClass()

def run_full_suite():
    run_full = hasattr(settings, 'SELENIUM_RUN_FULL_SUITE') and settings.SELENIUM_RUN_FULL_SUITE
    return [run_full, "Skipping minor selenium tests"]

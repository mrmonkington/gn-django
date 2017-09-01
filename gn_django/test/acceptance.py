import unittest, time, sys
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from gn_django.url.utils import convert_to_camelcase
from .selenium import GNRemote, browser_manager

RESOLUTIONS = {
    'desktop': '1920x1080',
    'portable_landscape': '1024x768',
    'portable_portrait': '768x1024',
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
        cls.browser = browser_manager.get_browser(capabilities, test_name=cls.__name__)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if hasattr(settings, "SELENIUM_PERSISTENT_BROWSERS") and settings.SELENIUM_PERSISTENT_BROWSERS:
            pass
        else:
            cls.browser.quit()
            
            

def run_full_suite():
    run_full = hasattr(settings, 'SELENIUM_RUN_FULL_SUITE') and settings.SELENIUM_RUN_FULL_SUITE
    return [run_full, "Skipping minor selenium tests"]

def build_test_cases(name, test_mixins, browsers, resolutions, module_name):
    test_cases = []
    for browser in browsers:
        for resolution in resolutions:
            test_parents = tuple(test_mixins + [AcceptanceTestCase])
            test_case_name = ' '.join([browser, resolution, 'Test Case'])
            test_case_name = name + convert_to_camelcase(test_case_name)
            class_attrs = {
                'browser_name': browser,
                'resolution': RESOLUTIONS[resolution],
            }
            test_case = type(test_case_name, test_parents, class_attrs)
            test_cases.append(test_case)
            # Skip non-major test cases if run_full_suite() evaluates to false
            browser_resolution_is_major = browser == 'chrome' and resolution == 'desktop'
            if not browser_resolution_is_major:
                test_case = unittest.skipUnless(*run_full_suite())(test_case)
    module = sys.modules[module_name]
    for test_case in test_cases:
        setattr(module, test_case.__name__, test_case)

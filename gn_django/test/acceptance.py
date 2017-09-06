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
    TestCase class which has a Remote selenium browser attribute, at a defined 
    resolution.

    Subclasses of AcceptanceTestCase can define class attributes as follows:
     * ``browser_name`` - 'chrome' or 'firefox'
     * ``resolution`` - String of format '1920x1080'
    """

    browser_name = 'chrome'
    resolution = RESOLUTIONS['desktop']
    element_scroll_behavior = 'bottom'

    @classmethod
    def setUpClass(cls):
        if hasattr(settings, "SELENIUM_APP_HOST"):
            cls.host = settings.SELENIUM_APP_HOST
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

def build_test_cases(name_prefix, test_mixins, browsers, resolutions, module_name):
    """
    Builds a set of concrete AcceptanceTestCase classes, given mixin classes 
    of test methods, browser/resolutions that should be run
    and the module on which test classes should be defined.

    Args:
      * ``name_prefix`` - string - The prefix that should be given to all test
        case classes.
      * ``test_mixins`` - iterable - Iterable of mixin classes.
      * ``browsers`` - iterable - Iterable of browser names.
      * ``resolutions`` - iterable - Iterable of resolution labels.
      * ``module_name`` - string - Name of the module to define test case
        classes on.

    Returns:
      None.  Test cases are defined on the given python module.

    Example:

    .. code-block:: python

        # In tests/test_user_browse.py

        acceptance.build_test_cases(
            name='UserBrowse', 
            test_mixins=[GeneralUserBrowseTestsMixin, DesktopUserBrowseTestsMixin], 
            browsers=['chrome', 'firefox'], 
            resolutions=['desktop', 'portable_portrait', 'portable_landscape'], 
            module_name=__name__
        )
        # Defines: 
        # UserBrowseChromeDesktopTestCase, UserBrowseChromePortablePortraitTestCase,
        # UserBrowseChromePortableLandscapeTestCase, UserBrowseFirefoxDesktopTestCase,
        # UserBrowseFirefoxPortablePortraitTestCase, UserBrowseFirefoxPortableLandscapeTestCase.

    """
    test_cases = []
    for browser in browsers:
        for resolution in resolutions:
            test_parents = tuple(test_mixins + [AcceptanceTestCase])
            test_case_name = ' '.join([browser, resolution, 'Test Case'])
            test_case_name = name_prefix + convert_to_camelcase(test_case_name)
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

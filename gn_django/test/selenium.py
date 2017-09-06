import time, atexit

from django.conf import settings

from selenium.common.exceptions import StaleElementReferenceException, InvalidSelectorException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

def wait_for(condition_function, *args, **kwargs):
    start_time = time.time() 
    while time.time() < start_time + 3: 
        if condition_function(*args, **kwargs): 
            return True 
        else: 
            time.sleep(0.1) 
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


def link_has_gone_stale(link):
    try:
        # poll the link with an arbitrary call
        link.find_elements_by_id('doesnt-matter') 
        return False
    except (StaleElementReferenceException, InvalidSelectorException):
        return True


class GNWebElement(WebElement):
    """
    Custom WebElement class enabling extended element find/interaction shortcuts.

    Interaction calls will generally scroll the browser so that the element is
    in the viewport, before interaction functionality is run.
    """

    def __init__(self, *args, **kwargs):
        self.element_scroll_behavior = None
        if 'element_scroll_behavior' in kwargs.keys():
            self.element_scroll_behavior = kwargs.pop('element_scroll_behavior')
        super().__init__(*args, **kwargs)

    def scroll_to_element(self):
        """
        If element scroll behaviour has been defined, use javascript to scroll
        an element in to the view port.
        """
        if self.element_scroll_behavior == 'bottom':
            self._parent.execute_script(
                "arguments[0].scrollIntoView(false);", self)
        if self.element_scroll_behavior == 'top':
            self._parent.execute_script(
                "arguments[0].scrollIntoView(true);", self)
        
    def click(self):
        self.scroll_to_element()
        return super().click()

    def send_keys(self, *args, **kwargs):
        self.scroll_to_element()
        return super().send_keys(*args, **kwargs)

    def wait_for_new_page(self):
        """
        Wait for a new page to load in the browser.
        """
        wait_for(link_has_gone_stale, self)

    def click_to_new_page(self):
        """
        Click a link which links through to a new page and wait for the 
        page to load.
        """
        result = self.click()
        self.wait_for_new_page()
        return result

    def send_enter(self):
        """
        Send the enter key and wait for a new page load.
        """
        self.send_keys(u'\ue007')
        self.wait_for_new_page()


class GNRemote(webdriver.Remote):
    """
    Selenium Remote subclass which uses our custom GNWebElement class for
    interacting with dom elements.

    This allows us to specify custom element scroll behaviour - meaning we 
    can ensure an element has been scrolled in to view before interacting
    with it.
    """

    _web_element_cls = GNWebElement

    def __init__(self, *args, **kwargs):
        self.element_scroll_behavior = None
        if 'element_scroll_behavior' in kwargs.keys():
            self.element_scroll_behavior = kwargs.pop('element_scroll_behavior')
        super().__init__(*args, **kwargs)

    def create_web_element(self, element_id):
        """
        Creates a web element with the specified `element_id`.
        """
        return self._web_element_cls(self, element_id, w3c=self.w3c, 
            element_scroll_behavior=self.element_scroll_behavior)

class BrowserManager:
    """
    Provides instantiated selenium browser objects, given a requested set of
    capabilities.

    This manager instantiates one browser per test case.
    """

    def _get_dimensions_and_capabilities(self, capabilities, test_name):
        capabilities = capabilities.copy()
        dimensions = [int(dimension) for dimension in capabilities['screenResolution'].split('x')]
        width_offset = 0
        height_offset = 0
        if capabilities['browserName'] == 'firefox':
            height_offset = 71
        if capabilities['browserName'] == 'chrome':
            width_offset = 11
            height_offset = 87
        dimensions[0] += width_offset
        dimensions[1] += height_offset
        capabilities['name'] = test_name
        capabilities['screenResolution'] = '2100x1200'
        return (dimensions, capabilities)
        
    def get_browser(self, capabilities, test_name):
        """
        Get an instantiated browser, given a set of capabilities.

        Args:
          * ``capabilities`` - dict - Selenium capabilities dictionary;
            http://selenium-python.readthedocs.io/api.html#desired-capabilities
          * ``test_name`` - string - test name for the current test case.

        Returns:
          An instantiated selenium browser.
        """
        dimensions, capabilities = self._get_dimensions_and_capabilities(capabilities, test_name)
        element_scroll_behavior = capabilities.get('elementScrollBehavior')
        kwargs = {
            'command_executor': "http://%s:4444/wd/hub" % settings.SELENIUM_HUB_HOST,
            'desired_capabilities': capabilities,
        }
        if element_scroll_behavior:
            kwargs['element_scroll_behavior'] = element_scroll_behavior
        browser = GNRemote(**kwargs)
        browser.implicitly_wait(1)
        width, height = int(dimensions[0]), int(dimensions[1])
        browser.set_window_size(width, height)
        return browser
    
    
class PersistentBrowserManager(BrowserManager):
    """
    Much like the standard BrowserManager, but attempts to reuse 
    browser instances by reusing existing browsers which match a particular
    set of capabilities.
    """
    
    def __init__(self):
        self._browsers = {}

    def _hash_capabilities(self, capabilities):
        return hash(frozenset(capabilities.items()))

    def _get_dimensions_and_capabilities(self, capabilities, test_name):
        dimensions, capabilities = super()._get_dimensions_and_capabilities(capabilites, test_name)
        capabilities['name'] = capabilities['browserName'] + ' ' + capabilities['screenResolution']
        return (dimensions, capabilities)

    def get_browser(self, capabilities, test_name):
        """
        Get an instantiated browser, given a set of capabilities.

        Args:
          * ``capabilities`` - dict - Selenium capabilities dictionary;
            http://selenium-python.readthedocs.io/api.html#desired-capabilities
          * ``test_name`` - string - test name for the current test case.

        Returns:
          An instantiated selenium browser.
        """
        capability_hash = self._hash_capabilities(capabilities)
        dimensions, capabilities = self._get_dimensions_and_capabilities(capabilities, test_name)
        browser = self._browsers.get(capability_hash)
        if browser:
            browser.delete_all_cookies()
        else:
            browser = super().get_browser(capabilities, test_name)
        return browser

    def cleanup(self):
        for browser in self._browsers.values():
            browser.quit()

if hasattr(settings, "SELENIUM_PERSISTENT_BROWSERS") and settings.SELENIUM_PERSISTENT_BROWSERS:
    browser_manager = PersistentBrowserManager()
    atexit.register(browser_manager.cleanup)
else:
    browser_manager = BrowserManager()


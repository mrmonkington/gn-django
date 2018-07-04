.. _gn-django-package-test:

Test
====

The ``test`` package contains functionality for aiding with testing python/django
libraries and applications.

Acceptance tests in django
--------------------------

Acceptance tests ensure that some functionality is working and usable for an 
end user.  In our case, this is best achieved by using automated browser testing
through selenium.

gn-django provides an ``AcceptanceTestCase`` class for these purposes.  This handles
instantiation of a selenium Remote driver based on class attributes set on the
test case class, namely ``browser_name`` and ``resolution``.  A subclass of
``AcceptanceTestCase`` is thus tied to a single browser/resolution combination.

.. autoclass:: gn_django.test.acceptance.AcceptanceTestCase
   :members:

.. note::

    **Splinter or raw selenium**
    
    You should set a class attribute ``use_splinter=True`` on the ``AcceptanceTestCase``
    subclass - this will mean that ``self.browser`` is a browser instance provided
    by the splinter library.  http://splinter.readthedocs.io/en/latest/index.html
    Splinter is a very helpful library which provides a lot of convenience methods
    on top of the standard selenium API.  It's generally a much better interface
    for quickly writing test cases.


Actually, a set of tests are generally applicable to a multitude of
browser/resolution combinations.  To avoid duplication of test code or heavy
boilerplate, a helper function ``build_test_cases()`` is supplied.

.. autofunction:: gn_django.test.acceptance.build_test_cases

So generally, the best approach for defining acceptance tests is to define
test mixin classes and use ``build_test_cases()`` to build the concrete test
classes.  It's likely that a subset of test functionality is applicable to all
browser types/resolutions; this should be encapsulated in a test mixin.  
Mobile-specific test methods can be encapsulated in a second mixin class, and
desktop-specific methods can be defined in a third mixin class.

The concrete classes can then be built with use of ``build_test_cases()`` - 
which combines the mixins specified for each permutation of browser/resolution
supplied.

.. note::

    **Forcing splinter**

    If you're using the ``build_test_cases()`` function, you can enforce the
    use of splinter by setting a kwarg ``use_splinter=True`` when calling the
    function.
    

Selenium
^^^^^^^^

**Deprecated: It's strongly advised to use splinter (``use_splinter=True``) as
opposed to using our extended functionality for raw selenium.**

gn-django supplies some helper functionality for using the selenium webdriver API.

By default, browser instances available on ``AcceptanceTestCase`` classes are instances
of ``GNRemote``:

.. autoclass:: gn_django.test.selenium.GNRemote
   :members:

The web elements returned by ``GNRemote`` objects through common 
``find_element_*`` methods are instances of ``GNWebElement``, which offers
a number of helpers:

.. autoclass:: gn_django.test.selenium.GNWebElement
   :members:

Settings
^^^^^^^^

To use gn-django's ``AcceptanceTestCase`` and selenium functionality, there are
a number of django settings which should be configured.

``SELENIUM_RUN_TESTS`` - boolean - No ``AcceptanceTestCase`` subclasses will
be tested if this is not set to ``True``.  This is handy because selenium tests
take so long to run, during the course of development it will be generally better
to only run the other test layers.

``SELENIUM_HUB_HOST`` - string - The hostname for the selenium hub instance used
to drive browsers.

``SELENIUM_APP_HOST`` - string - The hostname which resolves to the django 
test application.  If you're running everything locally, this will just be 
``'localhost'``.  If you're running through docker containers, it's likely to
be the name of your django app container.

``SELENIUM_RUN_FULL_SUITE`` - boolean - All acceptance test cases will run 
if this is set to ``True``.  Otherwise, only chrome desktop test cases
will be run.

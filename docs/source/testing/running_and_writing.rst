Testing GN Django 
=================

Tests are located in ``tests/`` which doubles up as a barebones django project.

Running tests
-------------

Tests can be run with simply ``do tests`` in the gn-django root.  This will trigger
``django-admin test tests`` - running all of the tests contained within the 
``tests/`` directory.

**NOTE:** You need a virtualenv active which has the requisite requirements 
installed from the project root's ``requirements.txt``.

To run just a subset of tests, you can trigger them in the normal django way, e.g::
    
    django-admin test tests.test_template

Writing tests
-------------

Tests in the repository should follow the `general guidelines for platform tests <https://github.com/gamernetwork/devops/wiki/Platform-Testing>`_.

Tests for the various components within gn-django should be written in
files under ``tests/`` of the format ``test_*.py`` - this will mean that django
automatically identifies the test cases and runs them.


Jinja vs Django Templates
=========================

Why?
----

Django's built-in templating is perfectly usable for the majority of web 
development needs, however there are some benefits in using jinja instead:
 - **Jinja is not very opinionated about limiting logic in templates.**  Keeping template
   logic to a minimum is a good guideline to follow, but sometimes a little bit
   of template logic can be handy - especially when the backend isn't fully
   implemented yet.
 - **Jinja is built to be easy to extend.**  Jinja offers good documentation and
   hooks for extending the template syntax itself, how loaders look up templates,
   filters/globals etc.  We need this flexibility in our template engine of choice.
 - **Jinja has more features than django templates.**  
   `macros <http://jinja.pocoo.org/docs/2.9/templates/#macros>`_, 
   `assignments <http://jinja.pocoo.org/docs/2.9/templates/#assignments>`_, 
   `expressions <http://jinja.pocoo.org/docs/2.9/templates/#expressions>`_,
   `tests <http://jinja.pocoo.org/docs/2.9/templates/#tests>`_,
   `comments <http://jinja.pocoo.org/docs/2.9/templates/#comments>`_ and
   `whitespace control <http://jinja.pocoo.org/docs/2.9/templates/#whitespace-control>`_
   are either non-existant or much less useful in django templates.

Drawbacks of using jinja
------------------------

Django allows swapping out it's template engine to jinja with no problems.  However,
the main drawback of using a different template engine than django's own is that
all django documentation assumes you are using django's template engine.  So 
syntax needs to be re-jigged when this is copy/pasted and any libraries that have
template integration will sometimes need a little bit of extra effort to get working
with jinja.

Some of the common practical differences are:

 - Jinja has no ``{% load .. %}`` tag - all globals/filters are available
   in scope automatically.
 - Django's template syntax for parameterised filters is as follows:
   ``{{foo|cut:10}}``
   Whereas jinja's is:
   ``{{foo|cut(10)}}``
 - Third party libraries which offer django filters, need to instead be registered 
   for jinja.  This can be achieved as described in 
   :ref:`the following section <adapting-third-party-for-jinja>`.

.. adapting-third-party-for-jinja::

Adapting third-party django filters/tags to use in jinja
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To register a global or filter from a third party library for use in jinja, there
are two mechanisms that could be used:
 - Register the global/filter just for your current django project, using 
   :ref:`this mechanism <registering-jinja-per-application-globals-filters>`.
 - If the third-party library is included as a gn-django dependency, 
   register the global/filter as a default for gn-django using
   :ref:`this mechanism <extending-jinja-globals-filters>`.

Template tags are a little more complex, and require creating a jinja extension.
This is described extensively in the jinja docs `here <http://jinja.pocoo.org/docs/2.9/extensions/#module-jinja2.ext>`_.

Regardless of the method used, this should just be a case of wrapping the python
function in the third party library with a simple proxy class/function.


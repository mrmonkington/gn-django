.. templatefilter:: yesno

``yesno``
---------

Maps values for ``True``, ``False``, and (optionally) ``None``, to the strings
"yes", "no", "maybe", or a custom mapping passed as a comma-separated list, and
returns one of those strings according to the value:

For example::

    {{ value|yesno:"yeah,no,maybe" }}

==========  ======================  ===========================================
Value       Argument                Outputs
==========  ======================  ===========================================
``True``                            ``yes``
``True``    ``"yeah,no,maybe"``     ``yeah``
``False``   ``"yeah,no,maybe"``     ``no``
``None``    ``"yeah,no,maybe"``     ``maybe``
``None``    ``"yeah,no"``           ``no`` (converts ``None`` to ``False``
                                    if no mapping for ``None`` is given)
==========  ======================  ===========================================

Internationalization tags and filters
=====================================

Django provides template tags and filters to control each aspect of
:doc:`internationalization </topics/i18n/index>` in templates. They allow for
granular control of translations, formatting, and time zone conversions.

``i18n``
--------

This library allows specifying translatable text in templates.
To enable it, set :setting:`USE_I18N` to ``True``, then load it with
``{% load i18n %}``.

See :ref:`specifying-translation-strings-in-template-code`.

``l10n``
--------

This library provides control over the localization of values in templates.
You only need to load the library using ``{% load l10n %}``, but you'll often
set :setting:`USE_L10N` to ``True`` so that localization is active by default.

See :ref:`topic-l10n-templates`.

``tz``
------

This library provides control over time zone conversions in templates.
Like ``l10n``, you only need to load the library using ``{% load tz %}``,
but you'll usually also set :setting:`USE_TZ` to ``True`` so that conversion
to local time happens by default.

See :ref:`time-zones-in-templates`.

Other tags and filters libraries
================================

Django comes with a couple of other template-tag libraries that you have to
enable explicitly in your :setting:`INSTALLED_APPS` setting and enable in your
template with the :ttag:`{% load %}<load>` tag.

``django.contrib.humanize``
---------------------------

A set of Django template filters useful for adding a "human touch" to data. See
:doc:`/ref/contrib/humanize`.

``static``
----------


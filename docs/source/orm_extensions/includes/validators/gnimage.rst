.. class:: GamerNetworkImageValidator

    The :code:`GamerNetworkImageValidator` extends the Django `URLValidator <https://docs.djangoproject.com/en/1.11/ref/validators/#urlvalidator>`_,
    but also checks that the URL is an image served from a Gamer Network CDN.
    Takes an optional parameter ``patterns``, to set which URL patterns are acceptable Gamer Network CDN urls.
    If not set this will default to:

    .. code-block:: python

      [
          r'^(http)?s?\:?\/\/[a-zA-Z0-9-_]+.gamer\-network.net/',
          r'^(http)?s?\:?\/\/[a-zA-Z0-9-_]+.eurogamer.net/',
      ]

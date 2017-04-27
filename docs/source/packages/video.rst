.. _video-library:

Video
=====

YouTube
-------

The YouTube library can be accessed by importing :code:`gn_django.video.youtube`

.. class:: YoutubeField

  See :ref:`YoutubeField <youtube-field>`

.. class:: YoutubeValidator

  See :ref:`YoutubeValidator <youtube-validator>`

.. function:: get_id(url)

  Extracts the 11 character ID from a YouTube URL, if valid.
  If no ID is found, :code:`None` will be returned.

.. function:: get_thumb(url, type = 'mqdefault')

  Returns the URL of the thumbnail for the video, if valid. If the URL is
  not a valid YouTube URL, :code:`None` will be returned.

  YouTube has an array of different thumbnails for each video, which can be declared
  by the :code:`type` parameter. YouTube provides the following types:

  - :code:`default` - Small default
  - :code:`mqdefault` - Medium default (wide screen)
  - :code:`maxresdefault` - High resolution default
  - :code:`0` - Large thumbnail
  - :code:`1` - Small thumbnail (first variant)
  - :code:`2` - Small thumbnail (second variant)
  - :code:`3` - Small thumbnail (third variant)

import unittest
from itertools import chain

from gn_django.video import twitch, youtube


class TestTwitch(unittest.TestCase):
    valid_channel_urls = {
        'zeldaspeedruns': 'https://www.twitch.tv/zeldaspeedruns',
        'argick': 'https://www.twitch.tv/argick?autoplay=true',
        'z0wrr3rwDWxG': 'https://www.twitch.tv/z0wrr3rwDWxG',
    }
    valid_vod_urls = {
        '1': 'https://www.twitch.tv/videos/1',
        '1337': 'https://www.twitch.tv/videos/1337/?utm_source=google',
        '467234': 'https://www.twitch.tv/videos/467234',
    }
    invalid_urls = (
        'https://www.twitch.tv',
        'https://www.twitch.tv/zeldaspeedruns/123456',
        'https://www.twitch.tv/watchthischannelitsnicebuttoolong',
        'https://www.twitch.tv/tv',
        'https://www.twitch.tv/videos/zeldaspeedruns',
        'https://www.twitch.tv/videos/-1',
        'https://www.example.com/tjrIMKo-1Ds',
        'https://www.vimeo.com/tjrIMKo-1Ds',
        'https://www.youtube.com/watch?v=tjrIMKo-1Ds',
        'https://youtu.be/tjrIMKo-1Ds',
    )

    def test_get_channel(self):
        for expected, valid_url in self.valid_channel_urls.items():
            self.assertEqual(expected, twitch.get_channel(valid_url))

        for url in chain(self.valid_vod_urls.values(), self.invalid_urls):
            self.assertIsNone(twitch.get_channel(url))

    def test_get_vod(self):
        for expected, valid_url in self.valid_vod_urls.items():
            self.assertEqual(expected, twitch.get_vod(valid_url))

        for invalid_url in chain(self.valid_channel_urls.values(), self.invalid_urls):
            self.assertIsNone(twitch.get_vod(invalid_url))


class TestYoutube(unittest.TestCase):
    """
    Test cases for Youtube helper functions
    """
    valid_urls = (
        'https://www.youtube.com/watch?v=tjrIMKo-1Ds',
        'http://www.youtube.com/watch?v=tjrIMKo-1Ds',
        'https://youtu.be/tjrIMKo-1Ds',
        'http://youtu.be/tjrIMKo-1Ds',
        'https://www.youtube.com/embed/tjrIMKo-1Ds',
        'http://www.youtube.com/embed/tjrIMKo-1Ds',
        'https://www.youtube.com/v/tjrIMKo-1Ds?version=3&autohide=1',
        'http://www.youtube.com/v/tjrIMKo-1Ds?version=3&autohide=1',
    )

    invalid_urls = (
        'https://www.example.com/tjrIMKo-1Ds',
        'https://www.vimeo.com/tjrIMKo-1Ds',
        'https://www.youtube.com'
    )

    img_formats = (
        'default',
        'mqdefault',
        'maxresdefault',
        '0',
        '1',
        '2',
        '3',
    )

    def test_get_id(self):
        """
        Test that all Youtube URL formats return the correct video ID
        """
        expected = 'tjrIMKo-1Ds'

        for url in self.valid_urls:
            vid = youtube.get_id(url)
            self.assertEqual(expected, vid)

    def test_get_id_invalid(self):
        """
        Test that invalid Youtube video URLs return `None`
        """
        for url in self.invalid_urls:
            self.assertEqual(None, youtube.get_id(url))

    def test_get_thumb(self):
        """
        Test that all Youtube URL format return all Youtube thumbnail formats
        """
        expected = 'http://i3.ytimg.com/vi/tjrIMKo-1Ds/%s.jpg'

        for url in self.valid_urls:
            for f in self.img_formats:
                thumb = youtube.get_thumb(url, f)
                self.assertEqual(expected % f, thumb)

    def test_get_thumb_invalid(self):
        """
        Test that invalid Youtube video URLs return `None`
        """
        for url in self.invalid_urls:
            for f in self.img_formats:
                thumb = youtube.get_thumb(url, f)
                self.assertEqual(None, thumb)

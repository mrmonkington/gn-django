from django.test import TestCase

from gn_django.utils import csv_download_response

class CsvDownloadResponseTest(TestCase):
    def test_csv_response(self):
        data = (
            ('Byte', '& Barq'),
            ('Dr', 'Coyle'),
            ('Hedlok', ''),
            ('Helix', ''),
        )
        response, writer = csv_download_response(('First Name', 'Second Name'), data, 'arms-roster')
        expected_content = b"First Name,Second Name\r\nByte,& Barq\r\nDr,Coyle\r\nHedlok,\r\nHelix,\r\n"
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response.content, expected_content)
        self.assertEqual(writer.__class__.__module__, '_csv')
        self.assertEqual(writer.__class__.__name__, 'writer')

    def test_csv_response_inconsistent_data(self):
        data = (
            ('Byte', '& Barq'),
            ('Dr', 'Coyle'),
            ('Hedlok',),
            ('Helix',),
        )
        response, writer = csv_download_response(('First Name', 'Second Name'), data, 'arms-roster')
        expected_content = b"First Name,Second Name\r\nByte,& Barq\r\nDr,Coyle\r\nHedlok\r\nHelix\r\n"
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response.content, expected_content)
        self.assertEqual(writer.__class__.__module__, '_csv')
        self.assertEqual(writer.__class__.__name__, 'writer')
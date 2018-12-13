from django.test import TestCase

from gn_django.utils import csv_download_response

class CsvDownloadResponseTest(TestCase):
    def test_csv_response(self):
        self.data = (
            ('Byte', '& Barq'),
            ('Dr', 'Coyle'),
            ('Hedlok', ''),
            ('Helix', ''),
        )
        response, writer = csv_download_response(('First Name', 'Second Name'), data, 'arms-roster')
        expected_content = """First Name,Second Name
Byte,& Barq
Dr,Coyle
Hedlok,
Helix,
"""
        self.assertEqual(response.content_type, 'text/csv')
        self.assertEqual(response.content.decode('utf-8'), expected_content)

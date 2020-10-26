from django.test import TestCase

from gn_django.utils import csv_download_response, csv_download_response_dict


class CSVDownloadResponseTest(TestCase):

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

    def test_csv_response_dict(self):
        data = [
            {
                'First Name': 'Byte',
                'Second Name': '& Barq',
            },
            {
                'First Name': 'Dr',
                'Second Name': 'Coyle',
            },
            {
                'First Name': 'Hedlok',
                'Second Name': '',
            },
            {
                'First Name': 'Helix',
                'Second Name': '',
            },
        ]
        response, writer = csv_download_response_dict(data, 'arms-roster')
        expected_content = b"First Name,Second Name\r\nByte,& Barq\r\nDr,Coyle\r\nHedlok,\r\nHelix,\r\n"
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response.content, expected_content)

    def test_csv_response_dict_data_empty(self):
        data = []
        with self.assertRaises(ValueError):
            response, writer = csv_download_response_dict(data, 'arms-roster')

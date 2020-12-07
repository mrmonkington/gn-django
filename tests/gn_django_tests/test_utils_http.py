from django.test import TestCase

from gn_django.utils import determine_remote_ip, csv_download_response, csv_download_response_dict


class DetermineRemoteIPTest(TestCase):
    def test_determine_remote_ip(self):
        factory = RequestFactory()

        # No appropriate data: returns the default IP.
        request = factory.get('/')
        self.assertEqual('127.0.0.1', determine_remote_ip(request))

        # Test with X-Client-Ip header.
        request = factory.get('/', HTTP_X_CLIENT_IP='123.4.56.7')
        self.assertEqual('123.4.56.7', determine_remote_ip(request))

        # Test with REMOTE_ADDR metadata.
        request = factory.get('/', REMOTE_ADDR='2001:db8:ff02:aa1::')
        self.assertEqual('2001:db8:ff02:aa1::', determine_remote_ip(request))

        # Test with both X-Client-Ip and REMOTE_ADDR (the header takes precedence).
        request = factory.get('/',
                              HTTP_X_CLIENT_IP='123.4.56.7',
                              REMOTE_ADDR='2001:db8:ff02:aa1::')
        self.assertEqual('123.4.56.7', determine_remote_ip(request))


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

    def test_csv_response_dict_irregular_dicts(self):
        data = [
            {
                'First Name': 'Byte',
            },
            {
                'Second Name': 'Coyle',
            },
            {
                'First Name': 'Hedlok',
                'Second Name': '',
            },
        ]
        response, writer = csv_download_response_dict(data, 'arms-roster')
        expected_content = b"First Name,Second Name\r\nByte,\r\n,Coyle\r\nHedlok,\r\n"
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response.content, expected_content)

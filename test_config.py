#!/usr/bin/python3

from io import StringIO
from unittest.mock import mock_open
from unittest.mock import MagicMock
from unittest.mock import patch
import unittest

from config import Config

class TestConfig(unittest.TestCase):

    def test_default(self):
        config = Config('fake.json')
        self.assertEqual(config.console.type, 'serial')
        self.assertEqual(config.console.path, '/dev/ttyUSB0')
        self.assertEqual(config.console.login, 'root')
        self.assertEqual(config.console.password, 'password')
        self.assertEqual(config.interval, 30)

    def test_fullconfig(self):
        TEST_JSON_TEXT = '{"console":{"path":"/here","type":"any","login":"login","password":"ppp"},"interval":100}'
        with patch('config.open', mock_open(read_data=TEST_JSON_TEXT)) as m:
            config = Config('config.json')
            m.assert_called_with('config.json')
            self.assertEqual(config.console.type, 'any')
            self.assertEqual(config.console.path, '/here')
            self.assertEqual(config.console.login, 'login')
            self.assertEqual(config.console.password, 'ppp')
            self.assertEqual(config.interval, 100)

if __name__ == '__main__':
    unittest.main()
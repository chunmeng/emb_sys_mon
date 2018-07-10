import unittest

from common import parse_version

class TestCommon(unittest.TestCase):

    def test_parse_version(self):
        self.assertEqual(parse_version(""), '') # empty
        self.assertEqual(parse_version("ver 1.01.1.1"), '1.01.1.1')
        self.assertEqual(parse_version("version=0.1.1.0-build5"), '0.1.1.0-build5')
        self.assertEqual(parse_version("version=7.1.1.0test111"), '7.1.1.0test111')
        self.assertEqual(parse_version("[[[version 1.3.3-rc1\n\n\n"), '1.3.3-rc1')
        self.assertEqual(parse_version("[[[version 1.3.3-rc1_1.0.1+ Something else\n\n\n"), '1.3.3-rc1_1.0.1+') # Special case
        self.assertEqual(parse_version("This is awesome version string 1.3.3-rc1_1.0-1_xx?x* \f\fr"), '1.3.3-rc1_1.0-1_xx?x*') # Special case
        self.assertEqual(parse_version("[[[Some garbage4.1.3.3-rc1_debug_this_and_that Something else\n\n\n"), '4.1.3.3-rc1_debug_this_and_that')

if __name__ == '__main__':
    unittest.main()
# -*- coding: UTF-8 -*-

import unittest

from buildtools.utilites import tobool


class UtilitesTest(unittest.TestCase):
    def test_tobool(self):
        self.assertTrue(tobool(1))
        self.assertTrue(tobool(True))
        self.assertTrue(tobool(u'1'))
        self.assertTrue(tobool(u'True'))
        self.assertTrue(tobool('True'))
        self.assertTrue(tobool(u'true'))
        self.assertTrue(tobool('true'))

        self.assertFalse(tobool(0))
        self.assertFalse(tobool(u'0'))
        self.assertFalse(tobool(False))
        self.assertFalse(tobool(u'False'))
        self.assertFalse(tobool('False'))
        self.assertFalse(tobool(u'false'))
        self.assertFalse(tobool('false'))


if __name__ == '__main__':
    unittest.main()

# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.packageversion import checkVersion


class PackageVersionTest (unittest.TestCase):
    def test_equal(self):
        packageVersion = (1, 1)
        required = (1, 1)
        self.assertTrue(checkVersion(packageVersion, required))

    def test_great_minor(self):
        packageVersion = (1, 10)
        required = (1, 1)
        self.assertTrue(checkVersion(packageVersion, required))

    def test_less_minor(self):
        packageVersion = (1, 1)
        required = (1, 10)
        self.assertFalse(checkVersion(packageVersion, required))

    def test_great_major(self):
        packageVersion = (2, 10)
        required = (1, 1)
        self.assertFalse(checkVersion(packageVersion, required))

    def test_less_major(self):
        packageVersion = (1, 10)
        required = (2, 1)
        self.assertFalse(checkVersion(packageVersion, required))

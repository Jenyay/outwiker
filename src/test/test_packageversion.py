# -*- coding: UTF-8 -*-

import unittest

import outwiker.core.packageversion as pv


class PackageCheckVersionTest (unittest.TestCase):
    def test_equal(self):
        packageVersion = (1, 1)
        required = (1, 1)
        self.assertEqual(pv.checkVersion(packageVersion, required),
                         pv.VERSION_OK)

    def test_great_minor(self):
        packageVersion = (1, 10)
        required = (1, 1)
        self.assertEqual(pv.checkVersion(packageVersion, required),
                         pv.VERSION_OK)

    def test_less_minor(self):
        packageVersion = (1, 1)
        required = (1, 10)
        self.assertEqual(pv.checkVersion(packageVersion, required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)

    def test_great_major(self):
        packageVersion = (2, 10)
        required = (1, 1)
        self.assertEqual(pv.checkVersion(packageVersion, required),
                         pv.PLUGIN_MUST_BE_UPGRADED)

    def test_less_major(self):
        packageVersion = (1, 10)
        required = (2, 1)
        self.assertEqual(pv.checkVersion(packageVersion, required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)


class PackageCheckVersionAnyTest (unittest.TestCase):
    def test_ok_01(self):
        packageVersion = (1, 1)
        required = [(1, 1)]
        self.assertEqual(pv.checkVersionAny(packageVersion, required),
                         pv.VERSION_OK)

    def test_ok_02(self):
        packageVersion = (1, 1)
        required = [(1, 1), (2, 0)]
        self.assertEqual(pv.checkVersionAny(packageVersion, required),
                         pv.VERSION_OK)

    def test_ok_03(self):
        packageVersion = (2, 0)
        required = [(1, 1), (2, 0)]
        self.assertEqual(pv.checkVersionAny(packageVersion, required),
                         pv.VERSION_OK)

    def test_ok_04(self):
        packageVersion = (2, 0)
        required = []
        self.assertEqual(pv.checkVersionAny(packageVersion, required),
                         pv.VERSION_OK)

    def test_ok_05(self):
        packageVersion = (2, 0)
        required = None
        self.assertEqual(pv.checkVersionAny(packageVersion, required),
                         pv.VERSION_OK)

    def test_ok_06(self):
        packageVersion = (2, 10)
        required = [(2, 0)]
        self.assertEqual(pv.checkVersionAny(packageVersion, required),
                         pv.VERSION_OK)

    def test_fail_01(self):
        packageVersion = (2, 0)
        required = [(1, 1), (3, 0)]
        self.assertNotEqual(pv.checkVersionAny(packageVersion, required),
                            pv.VERSION_OK)

    def test_fail_02(self):
        packageVersion = (2, 10)
        required = [(2, 15)]
        self.assertEqual(pv.checkVersionAny(packageVersion, required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)

    def test_fail_03(self):
        packageVersion = (2, 0)
        required = [(1, 0)]
        self.assertEqual(pv.checkVersionAny(packageVersion, required),
                         pv.PLUGIN_MUST_BE_UPGRADED)


class CheckPackagesVersionTest (unittest.TestCase):
    def test_ok_01(self):
        packageversion_list = [(1, 0), (1, 0)]
        required = [[(1, 0)], [(1, 0)]]

        self.assertEqual(pv.checkAllPackagesVersions(packageversion_list,
                                                     required),
                         pv.VERSION_OK)

    def test_ok_02(self):
        packageversion_list = [(1, 10), (1, 10)]
        required = [[(1, 0)], [(1, 0)]]

        self.assertEqual(pv.checkAllPackagesVersions(packageversion_list,
                                                     required),
                         pv.VERSION_OK)

    def test_ok_03(self):
        packageversion_list = [(1, 10), (1, 10)]
        required = [[(1, 0), (2, 0)], [(1, 10)]]

        self.assertEqual(pv.checkAllPackagesVersions(packageversion_list,
                                                     required),
                         pv.VERSION_OK)

    def test_fail_01(self):
        packageversion_list = [(1, 0), (1, 0)]
        required = [[(1, 1)], [(1, 1)]]

        self.assertEqual(pv.checkAllPackagesVersions(packageversion_list,
                                                     required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)

    def test_fail_02(self):
        packageversion_list = [(1, 0), (1, 0)]
        required = [[(1, 1)], [(1, 0)]]

        self.assertEqual(pv.checkAllPackagesVersions(packageversion_list,
                                                     required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)

    def test_fail_03(self):
        packageversion_list = [(1, 0), (1, 0)]
        required = [[(1, 0)], [(1, 1)]]

        self.assertEqual(pv.checkAllPackagesVersions(packageversion_list,
                                                     required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)

    def test_fail_04(self):
        packageversion_list = [(1, 0), (2, 0)]
        required = [[(1, 0)], [(1, 0)]]

        self.assertEqual(pv.checkAllPackagesVersions(packageversion_list,
                                                     required),
                         pv.PLUGIN_MUST_BE_UPGRADED)

# -*- coding: utf-8 -*-

import unittest

import outwiker.core.packageversion as pv


class PackageCheckVersionTest (unittest.TestCase):
    def test_equal(self):
        current_api_version = (1, 1)
        required = (1, 1)
        self.assertEqual(pv.checkSingleVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_great_minor(self):
        current_api_version = (1, 10)
        required = (1, 1)
        self.assertEqual(pv.checkSingleVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_less_minor(self):
        current_api_version = (1, 1)
        required = (1, 10)
        self.assertEqual(pv.checkSingleVersion(current_api_version, required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)

    def test_great_major(self):
        current_api_version = (2, 10)
        required = (1, 1)
        self.assertEqual(pv.checkSingleVersion(current_api_version, required),
                         pv.PLUGIN_MUST_BE_UPGRADED)

    def test_less_major(self):
        current_api_version = (1, 10)
        required = (2, 1)
        self.assertEqual(pv.checkSingleVersion(current_api_version, required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)


class PackageCheckVersionAnyTest (unittest.TestCase):
    def test_ok_empty(self):
        current_api_version = (1, 1)
        required = []
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_ok_01(self):
        current_api_version = (1, 1)
        required = [(1, 1)]
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_ok_02(self):
        current_api_version = (1, 1)
        required = [(1, 1), (2, 0)]
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_ok_03(self):
        current_api_version = (2, 0)
        required = [(1, 1), (2, 0)]
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_ok_04(self):
        current_api_version = (2, 0)
        required = []
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_ok_05(self):
        current_api_version = (2, 0)
        required = None
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_ok_06(self):
        current_api_version = (2, 10)
        required = [(2, 0)]
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.VERSION_OK)

    def test_fail_01(self):
        current_api_version = (2, 0)
        required = [(1, 1), (3, 0)]
        self.assertNotEqual(pv.checkVersion(current_api_version, required),
                            pv.VERSION_OK)

    def test_fail_02(self):
        current_api_version = (2, 10)
        required = [(2, 15)]
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.OUTWIKER_MUST_BE_UPGRADED)

    def test_fail_03(self):
        current_api_version = (2, 0)
        required = [(1, 0)]
        self.assertEqual(pv.checkVersion(current_api_version, required),
                         pv.PLUGIN_MUST_BE_UPGRADED)

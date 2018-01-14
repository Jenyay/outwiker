# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.gui.menucontroller import MenuController, ROOT_MENU_ID


class MenuControllerTest(unittest.TestCase):
    def setUp(self):
        self.root = wx.Menu()
        self.controller = MenuController(self.root)

    def tearDown(self):
        pass

    def test_add_01(self):
        menu = wx.Menu()
        menu_id = 'menu_01'
        self.controller.addMenu(menu_id, menu)

        self.assertIn(menu_id, self.controller)
        self.assertEqual(self.controller[menu_id], menu)

    def test_add_02(self):
        menu_01 = wx.Menu()
        menu_id_01 = 'menu_01'
        self.controller.addMenu(menu_id_01, menu_01)

        menu_02 = wx.Menu()
        menu_id_02 = 'menu_02'
        self.controller.addMenu(menu_id_02, menu_02)

        self.assertIn(menu_id_01, self.controller)
        self.assertEqual(self.controller[menu_id_01], menu_01)

        self.assertIn(menu_id_02, self.controller)
        self.assertEqual(self.controller[menu_id_02], menu_02)

    def test_add_error(self):
        menu_01 = wx.Menu()
        menu_id = 'menu_01'
        menu_02 = wx.Menu()

        self.controller.addMenu(menu_id, menu_01)
        self.assertRaises(KeyError, self.controller.addMenu,
                          menu_id, menu_02)

    def test_get_error(self):
        self.assertRaises(KeyError, self.controller.__getitem__, 'menu_01')

    def test_remove_error_01(self):
        self.assertRaises(KeyError, self.controller.removeMenu, 'menu_01')

    def test_remove_error_02(self):
        self.assertRaises(KeyError, self.controller.removeMenu, ROOT_MENU_ID)

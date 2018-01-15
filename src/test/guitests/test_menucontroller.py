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

    def test_create_01(self):
        title = 'Menu title'
        menu_id = 'menu_id'

        self.controller.createSubMenu(menu_id, title)
        self.assertIn(menu_id, self.controller)
        self.assertTrue(isinstance(self.controller[menu_id], wx.Menu))

    def test_create_02_error(self):
        title = 'Menu title'

        self.assertRaises(KeyError, self.controller.createSubMenu,
                          ROOT_MENU_ID, title)

    def test_create_03_error(self):
        title = 'Menu title'
        menu_id = 'menu_id'

        self.controller.createSubMenu(menu_id, title)

        self.assertRaises(KeyError, self.controller.createSubMenu,
                          menu_id, title)

    def test_create_04(self):
        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        menu_01 = self.controller.createSubMenu(menu_id_01, title_01)
        menu_02 = self.controller.createSubMenu(menu_id_02, title_02)

        self.assertIn(menu_id_02, self.controller)
        self.assertEqual(self.controller[menu_id_01], menu_01)
        self.assertEqual(self.controller[menu_id_02], menu_02)

    def test_create_05(self):
        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        menu_01 = self.controller.createSubMenu(menu_id_01, title_01)
        menu_02 = self.controller.createSubMenu(menu_id_02, title_02,
                                                menu_id_01)

        self.assertIn(menu_id_02, self.controller)
        self.assertEqual(self.controller[menu_id_01], menu_01)
        self.assertEqual(self.controller[menu_id_02], menu_02)

    def test_remove_01_error(self):
        self.assertRaises(KeyError, self.controller.removeMenu, 'menu_01')

    def test_remove_02_error(self):
        self.assertRaises(KeyError, self.controller.removeMenu, ROOT_MENU_ID)

    def test_remove_03(self):
        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        self.controller.createSubMenu(menu_id_01, title_01)
        self.controller.createSubMenu(menu_id_02, title_02)

        self.controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, self.controller)
        self.assertIn(menu_id_02, self.controller)
        self.assertEqual(len(self.controller[ROOT_MENU_ID].GetMenuItems()), 1)

    def test_remove_04(self):
        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        self.controller.createSubMenu(menu_id_01, title_01)
        self.controller.createSubMenu(menu_id_02, title_02, menu_id_01)

        self.controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, self.controller)
        self.assertNotIn(menu_id_02, self.controller)
        self.assertEqual(len(self.controller[ROOT_MENU_ID].GetMenuItems()), 0)

    def test_remove_05(self):
        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        title_03 = 'Menu title_03'
        menu_id_03 = 'menu_id_03'

        self.controller.createSubMenu(menu_id_01, title_01)
        self.controller.createSubMenu(menu_id_02, title_02, menu_id_01)
        self.controller.createSubMenu(menu_id_03, title_03, menu_id_02)

        self.controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, self.controller)
        self.assertNotIn(menu_id_02, self.controller)
        self.assertNotIn(menu_id_03, self.controller)
        self.assertEqual(len(self.controller[ROOT_MENU_ID].GetMenuItems()), 0)

    def test_remove_06(self):
        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        title_03 = 'Menu title_03'
        menu_id_03 = 'menu_id_03'

        self.controller.createSubMenu(menu_id_01, title_01)
        self.controller.createSubMenu(menu_id_02, title_02, menu_id_01)
        self.controller.createSubMenu(menu_id_03, title_03, menu_id_01)

        self.controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, self.controller)
        self.assertNotIn(menu_id_02, self.controller)
        self.assertNotIn(menu_id_03, self.controller)
        self.assertEqual(len(self.controller[ROOT_MENU_ID].GetMenuItems()), 0)

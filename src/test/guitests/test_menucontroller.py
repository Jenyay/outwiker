# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.gui.menucontroller import MenuController, ROOT_MENU_ID


class MenuControllerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_01_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        menu = wx.Menu()
        menu_id = 'menu_01'
        controller.addMenu(menu_id, menu)

        self.assertIn(menu_id, controller)
        self.assertEqual(controller[menu_id], menu)

    def test_add_01_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        menu = wx.Menu()
        menu_id = 'menu_01'
        controller.addMenu(menu_id, menu)

        self.assertIn(menu_id, controller)
        self.assertEqual(controller[menu_id], menu)

    def test_add_02_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        menu_01 = wx.Menu()
        menu_id_01 = 'menu_01'
        controller.addMenu(menu_id_01, menu_01)

        menu_02 = wx.Menu()
        menu_id_02 = 'menu_02'
        controller.addMenu(menu_id_02, menu_02)

        self.assertIn(menu_id_01, controller)
        self.assertEqual(controller[menu_id_01], menu_01)

        self.assertIn(menu_id_02, controller)
        self.assertEqual(controller[menu_id_02], menu_02)

    def test_add_02_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        menu_01 = wx.Menu()
        menu_id_01 = 'menu_01'
        controller.addMenu(menu_id_01, menu_01)

        menu_02 = wx.Menu()
        menu_id_02 = 'menu_02'
        controller.addMenu(menu_id_02, menu_02)

        self.assertIn(menu_id_01, controller)
        self.assertEqual(controller[menu_id_01], menu_01)

        self.assertIn(menu_id_02, controller)
        self.assertEqual(controller[menu_id_02], menu_02)

    def test_add_error_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        menu_01 = wx.Menu()
        menu_id = 'menu_01'
        menu_02 = wx.Menu()

        controller.addMenu(menu_id, menu_01)
        self.assertRaises(KeyError, controller.addMenu,
                          menu_id, menu_02)

    def test_add_error_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        menu_01 = wx.Menu()
        menu_id = 'menu_01'
        menu_02 = wx.Menu()

        controller.addMenu(menu_id, menu_01)
        self.assertRaises(KeyError, controller.addMenu,
                          menu_id, menu_02)

    def test_get_error_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        self.assertRaises(KeyError, controller.__getitem__, 'menu_01')

    def test_get_error_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        self.assertRaises(KeyError, controller.__getitem__, 'menu_01')

    def test_create_01_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title = 'Menu title'
        menu_id = 'menu_id'

        controller.createSubMenu(menu_id, title)
        self.assertIn(menu_id, controller)
        self.assertTrue(isinstance(controller[menu_id], wx.Menu))

    def test_create_01_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title = 'Menu title'
        menu_id = 'menu_id'

        controller.createSubMenu(menu_id, title)
        self.assertIn(menu_id, controller)
        self.assertTrue(isinstance(controller[menu_id], wx.Menu))

    def test_create_02_error_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title = 'Menu title'

        self.assertRaises(KeyError, controller.createSubMenu,
                          ROOT_MENU_ID, title)

    def test_create_02_error_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title = 'Menu title'

        self.assertRaises(KeyError, controller.createSubMenu,
                          ROOT_MENU_ID, title)

    def test_create_03_error_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title = 'Menu title'
        menu_id = 'menu_id'

        controller.createSubMenu(menu_id, title)

        self.assertRaises(KeyError, controller.createSubMenu,
                          menu_id, title)

    def test_create_03_error_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title = 'Menu title'
        menu_id = 'menu_id'

        controller.createSubMenu(menu_id, title)

        self.assertRaises(KeyError, controller.createSubMenu,
                          menu_id, title)

    def test_create_04_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        menu_01 = controller.createSubMenu(menu_id_01, title_01)
        menu_02 = controller.createSubMenu(menu_id_02, title_02)

        self.assertIn(menu_id_02, controller)
        self.assertEqual(controller[menu_id_01], menu_01)
        self.assertEqual(controller[menu_id_02], menu_02)

    def test_create_04_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        menu_01 = controller.createSubMenu(menu_id_01, title_01)
        menu_02 = controller.createSubMenu(menu_id_02, title_02)

        self.assertIn(menu_id_02, controller)
        self.assertEqual(controller[menu_id_01], menu_01)
        self.assertEqual(controller[menu_id_02], menu_02)

    def test_create_05_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        menu_01 = controller.createSubMenu(menu_id_01, title_01)
        menu_02 = controller.createSubMenu(menu_id_02, title_02,
                                           menu_id_01)

        self.assertIn(menu_id_02, controller)
        self.assertEqual(controller[menu_id_01], menu_01)
        self.assertEqual(controller[menu_id_02], menu_02)

    def test_create_05_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        menu_01 = controller.createSubMenu(menu_id_01, title_01)
        menu_02 = controller.createSubMenu(menu_id_02, title_02,
                                           menu_id_01)

        self.assertIn(menu_id_02, controller)
        self.assertEqual(controller[menu_id_01], menu_01)
        self.assertEqual(controller[menu_id_02], menu_02)

    def test_remove_01_error_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        self.assertRaises(KeyError, controller.removeMenu, 'menu_01')

    def test_remove_01_error_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        self.assertRaises(KeyError, controller.removeMenu, 'menu_01')

    def test_remove_02_error_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        self.assertRaises(KeyError, controller.removeMenu, ROOT_MENU_ID)

    def test_remove_02_error_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        self.assertRaises(KeyError, controller.removeMenu, ROOT_MENU_ID)

    def test_remove_03_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02)

        controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, controller)
        self.assertIn(menu_id_02, controller)
        self.assertEqual(len(controller[ROOT_MENU_ID].GetMenus()), 1)

    def test_remove_03_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02)

        controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, controller)
        self.assertIn(menu_id_02, controller)
        self.assertEqual(len(controller[ROOT_MENU_ID].GetMenuItems()), 1)

    def test_remove_04_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02, menu_id_01)

        controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, controller)
        self.assertNotIn(menu_id_02, controller)
        self.assertEqual(len(controller[ROOT_MENU_ID].GetMenus()), 0)

    def test_remove_04_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02, menu_id_01)

        controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, controller)
        self.assertNotIn(menu_id_02, controller)
        self.assertEqual(len(controller[ROOT_MENU_ID].GetMenuItems()), 0)

    def test_remove_05_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        title_03 = 'Menu title_03'
        menu_id_03 = 'menu_id_03'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02, menu_id_01)
        controller.createSubMenu(menu_id_03, title_03, menu_id_02)

        controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, controller)
        self.assertNotIn(menu_id_02, controller)
        self.assertNotIn(menu_id_03, controller)
        self.assertEqual(len(controller[ROOT_MENU_ID].GetMenus()), 0)

    def test_remove_05_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        title_03 = 'Menu title_03'
        menu_id_03 = 'menu_id_03'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02, menu_id_01)
        controller.createSubMenu(menu_id_03, title_03, menu_id_02)

        controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, controller)
        self.assertNotIn(menu_id_02, controller)
        self.assertNotIn(menu_id_03, controller)
        self.assertEqual(len(controller[ROOT_MENU_ID].GetMenuItems()), 0)

    def test_remove_06_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        title_03 = 'Menu title_03'
        menu_id_03 = 'menu_id_03'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02, menu_id_01)
        controller.createSubMenu(menu_id_03, title_03, menu_id_01)

        controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, controller)
        self.assertNotIn(menu_id_02, controller)
        self.assertNotIn(menu_id_03, controller)
        self.assertEqual(len(controller[ROOT_MENU_ID].GetMenus()), 0)

    def test_remove_06_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        title_03 = 'Menu title_03'
        menu_id_03 = 'menu_id_03'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02, menu_id_01)
        controller.createSubMenu(menu_id_03, title_03, menu_id_01)

        controller.removeMenu(menu_id_01)

        self.assertNotIn(menu_id_01, controller)
        self.assertNotIn(menu_id_02, controller)
        self.assertNotIn(menu_id_03, controller)
        self.assertEqual(len(controller[ROOT_MENU_ID].GetMenuItems()), 0)

    def test_remove_07_menubar(self):
        root = wx.MenuBar()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        title_03 = 'Menu title_03'
        menu_id_03 = 'menu_id_03'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02, menu_id_01)
        controller.createSubMenu(menu_id_03, title_03, menu_id_02)

        controller.removeMenu(menu_id_03)
        controller.removeMenu(menu_id_02)
        controller.removeMenu(menu_id_01)

    def test_remove_07_menu(self):
        root = wx.Menu()
        controller = MenuController(root)

        title_01 = 'Menu title_01'
        menu_id_01 = 'menu_id_01'

        title_02 = 'Menu title_02'
        menu_id_02 = 'menu_id_02'

        title_03 = 'Menu title_03'
        menu_id_03 = 'menu_id_03'

        controller.createSubMenu(menu_id_01, title_01)
        controller.createSubMenu(menu_id_02, title_02, menu_id_01)
        controller.createSubMenu(menu_id_03, title_03, menu_id_02)

        controller.removeMenu(menu_id_03)
        controller.removeMenu(menu_id_02)
        controller.removeMenu(menu_id_01)

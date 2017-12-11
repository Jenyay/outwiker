# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.hotkey import HotKey
from outwiker.gui.hotkeyparser import HotKeyParser
from outwiker.gui.hotkeyoption import HotKeyOption
from outwiker.core.application import Application
from .basemainwnd import BaseMainWndTest


class TestAction (BaseAction):
    stringId = "test_action"

    def __init__ (self):
        self.runCount = 0


    @property
    def title (self):
        return u"Тестовый Action"


    @property
    def description (self):
        return u"Тестовый Action"


    def run (self, params):
        self.runCount += 1


class TestCheckAction (BaseAction):
    stringId = "test_check_action"

    def __init__ (self):
        self.runCount = 0


    @property
    def title (self):
        return u"Тестовый CheckAction"


    @property
    def description (self):
        return u"Тестовый CheckAction"


    def run (self, params):
        if params:
            self.runCount += 1
        else:
            self.runCount -= 1


class ActionControllerTest (BaseMainWndTest):
    def setUp (self):
        BaseMainWndTest.setUp (self)
        self.actionController = ActionController(self.wnd, Application.config)
        Application.config.remove_section (self.actionController.configSection)


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.config.remove_section (self.actionController.configSection)


    def testRegisterAction (self):
        action = TestAction()

        self.assertEqual (len (self.actionController.getActionsStrId()), 0)

        self.actionController.register (action)

        self.assertEqual (len (self.actionController.getActionsStrId()), 1)


    def testHotKeys (self):
        hotkey1 = HotKey ("F1")
        action1 = TestAction()

        hotkey2 = HotKey ("F2", ctrl=True)
        action2 = TestCheckAction()

        self.actionController.register (action1, hotkey1)
        self.actionController.register (action2, hotkey2)

        self.assertEqual (self.actionController.getHotKey(action1.stringId), hotkey1)
        self.assertEqual (self.actionController.getHotKey(action2.stringId), hotkey2)


    def testTitles (self):
        action1 = TestAction()
        action2 = TestCheckAction()

        self.actionController.register (action1)
        self.actionController.register (action2)

        self.assertEqual (self.actionController.getTitle(action1.stringId), action1.title)
        self.assertEqual (self.actionController.getTitle(action2.stringId), action2.title)


    def testAppendMenu (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)
        self._assertMenuItemExists (menu, action.title, None)


    def testAppendCheckMenu (self):
        action = TestCheckAction()
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.register (action)
        self.actionController.appendMenuCheckItem (action.stringId, menu)
        self._assertMenuItemExists (menu, action.title, None)


    def testRemoveAction (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.assertEqual (len (self.actionController.getActionsStrId()), 1)
        self._assertMenuItemExists (menu, action.title, None)
        self.assertEqual (toolbar.GetToolCount(), 1)

        self.actionController.removeAction (action.stringId)

        self.assertEqual (len (self.actionController.getActionsStrId()), 0)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)
        self.assertEqual (toolbar.GetToolCount(), 0)


    def testRemoveActionAndRun (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        menuItemId = self._getMenuItemId (action.stringId)
        toolItemId = self._getToolItemId (action.stringId)

        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 1)

        self._emulateButtonClick (toolItemId)
        self.assertEqual (action.runCount, 2)

        self.actionController.removeAction (action.stringId)

        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 2)

        self._emulateButtonClick (toolItemId)
        self.assertEqual (action.runCount, 2)


    def testRunAction (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)

        menuItemId = self._getMenuItemId (action.stringId)

        self._emulateMenuClick (menuItemId)

        self.assertEqual (action.runCount, 1)

        self.actionController.removeAction (action.stringId)

        # Убедимся, что после удаления пункта меню, событие больше не срабатывает
        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 1)


    def testAppendToolbarButton (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.assertEqual (toolbar.GetToolCount(), 1)

        self.actionController.removeAction (action.stringId)

        self.assertEqual (toolbar.GetToolCount(), 0)


    def testAppendToolbarCheckButton (self):
        action = TestCheckAction()
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarCheckButton (action.stringId,
                                                        toolbar,
                                                        image)

        self.assertEqual (toolbar.GetToolCount(), 1)

        self.actionController.removeAction (action.stringId)

        self.assertEqual (toolbar.GetToolCount(), 0)


    def testAppendToolbarCheckButtonAndRun (self):
        action = TestCheckAction()
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarCheckButton (action.stringId,
                                                        toolbar,
                                                        image)

        toolItemId = self._getToolItemId (action.stringId)

        self._emulateCheckButtonClick (toolItemId)
        self.assertEqual (action.runCount, 1)

        self._emulateCheckButtonClick (toolItemId)
        self.assertEqual (action.runCount, 0)

        self._emulateCheckButtonClick (toolItemId)
        self.assertEqual (action.runCount, 1)

        self.actionController.removeAction (action.stringId)


    def testCheckButtonAndMenuWithEvents (self):
        action = TestCheckAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarCheckButton (action.stringId,
                                                        toolbar,
                                                        image)
        self.actionController.appendMenuCheckItem (action.stringId, menu)

        menuItem = self._getMenuItem (action.stringId)
        toolItem = self._getToolItem (toolbar, action.stringId)
        toolItemId = self._getToolItemId (action.stringId)

        self.assertFalse (menuItem.IsChecked())
        self.assertFalse (toolItem.GetState())

        self._emulateCheckButtonClick (toolItemId)

        self.assertTrue (menuItem.IsChecked())
        self.assertTrue (toolItem.GetState())

        self._emulateCheckButtonClick (toolItemId)

        self.assertFalse (menuItem.IsChecked())
        self.assertFalse (toolItem.GetState())


    def testCheckButtonAndMenu (self):
        action = TestCheckAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarCheckButton (action.stringId,
                                                        toolbar,
                                                        image)
        self.actionController.appendMenuCheckItem (action.stringId, menu)

        menuItem = self._getMenuItem (action.stringId)
        toolItem = self._getToolItem (toolbar, action.stringId)

        self.assertFalse (menuItem.IsChecked())
        self.assertFalse (toolItem.GetState())
        self.assertEqual (action.runCount, 0)

        self.actionController.check (action.stringId, True)

        self.assertTrue (menuItem.IsChecked())
        self.assertTrue (toolItem.GetState())
        self.assertEqual (action.runCount, 1)

        self.actionController.check (action.stringId, True)

        self.assertTrue (menuItem.IsChecked())
        self.assertTrue (toolItem.GetState())
        self.assertEqual (action.runCount, 2)

        self.actionController.check (action.stringId, False)

        self.assertFalse (menuItem.IsChecked())
        self.assertFalse (toolItem.GetState())
        self.assertEqual (action.runCount, 1)

        self.actionController.check (action.stringId, False)

        self.assertFalse (menuItem.IsChecked())
        self.assertFalse (toolItem.GetState())
        self.assertEqual (action.runCount, 0)


    def testRemoveCheckMenu (self):
        action = TestCheckAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarCheckButton (action.stringId,
                                                        toolbar,
                                                        image)

        self.actionController.appendMenuCheckItem (action.stringId, menu)
        self.actionController.removeMenuItem (action.stringId)

        toolItem = self._getToolItem (toolbar, action.stringId)
        toolItemId = self._getToolItemId (action.stringId)

        self.assertFalse (toolItem.GetState())

        self._emulateCheckButtonClick (toolItemId)

        self.assertTrue (toolItem.GetState())

        self._emulateCheckButtonClick (toolItemId)

        self.assertFalse (toolItem.GetState())


    def testAppendToolbarButtonOnly (self):
        action = TestAction()
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.assertEqual (toolbar.GetToolCount(), 1)

        self.actionController.removeAction (action.stringId)

        self.assertEqual (toolbar.GetToolCount(), 0)


    def testAppendToolbarButtonAndRun (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        menuItemId = self._getMenuItemId (action.stringId)

        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 1)

        self.actionController.removeAction (action.stringId)

        self._emulateMenuClick (menuItemId)
        self.assertEqual (action.runCount, 1)


    def testAppendToolbarButtonOnlyAndRun (self):
        action = TestAction()
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        toolItemId = self._getToolItemId (action.stringId)

        self._emulateButtonClick (toolItemId)
        self.assertEqual (action.runCount, 1)

        self.actionController.removeAction (action.stringId)

        self._emulateButtonClick (toolItemId)
        self.assertEqual (action.runCount, 1)


    def testRemoveToolButton (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self._assertMenuItemExists (menu, action.title, None)

        self.actionController.removeToolbarButton (action.stringId)

        self.assertEqual (toolbar.GetToolCount(), 0)
        self._assertMenuItemExists (menu, action.title, None)


    def testRemoveToolButtonInvalid (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)

        self.assertEqual (toolbar.GetToolCount(), 0)
        self._assertMenuItemExists (menu, action.title, None)

        self.actionController.removeToolbarButton (action.stringId)

        self.assertEqual (toolbar.GetToolCount(), 0)
        self._assertMenuItemExists (menu, action.title, None)


    def testRemoveMenuItemInvalid (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)

        self.actionController.removeMenuItem (action.stringId)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)


    def testRemoveMenuItem (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action)
        self.actionController.appendMenuItem (action.stringId, menu)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self._assertMenuItemExists (menu, action.title, None)

        self.actionController.removeMenuItem (action.stringId)

        self.assertEqual (toolbar.GetToolCount(), 1)
        self.assertEqual (menu.FindItem (action.title), wx.NOT_FOUND)


    def testHotKeysDefaultMenu (self):
        action = TestAction()
        menu = self.wnd.mainMenu.fileMenu
        hotkey = HotKey ("T", ctrl=True)

        self.actionController.register (action, hotkey=hotkey)
        self.assertEqual (self.actionController.getHotKey (action.stringId), hotkey)

        self.actionController.appendMenuItem (action.stringId, menu)

        self._assertMenuItemExists (menu, action.title, hotkey)


    def testHotKeysDefaultToolBar (self):
        action = TestAction()
        hotkey = HotKey ("T", ctrl=True)
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action, hotkey=hotkey)
        self.assertEqual (self.actionController.getHotKey (action.stringId), hotkey)

        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.assertEqual (self._getToolItemLabel (toolbar, action.stringId),
                          u"{0} ({1})".format (action.title, HotKeyParser.toString (hotkey)))


    def testDisableTools (self):
        action = TestAction()
        hotkey = HotKey ("T", ctrl=True)
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        self.actionController.register (action, hotkey=hotkey)

        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        toolid = self._getToolItemId (action.stringId)

        self.actionController.enableTools (action.stringId, False)
        self.assertFalse (toolbar.GetToolEnabled (toolid))

        self.actionController.enableTools (action.stringId, True)
        self.assertTrue (toolbar.GetToolEnabled (toolid))


    def testDisableMenuItem (self):
        action = TestAction()
        hotkey = HotKey ("T", ctrl=True)
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.register (action, hotkey=hotkey)

        self.actionController.appendMenuItem (action.stringId, menu)

        menuItemId = self._getMenuItemId (action.stringId)

        self.actionController.enableTools (action.stringId, False)
        self.assertFalse (menu.IsEnabled (menuItemId))

        self.actionController.enableTools (action.stringId, True)
        self.assertTrue (menu.IsEnabled (menuItemId))


    def testDidableToolsAll (self):
        action = TestAction()
        hotkey = HotKey ("T", ctrl=True)
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"
        menu = self.wnd.mainMenu.fileMenu

        self.actionController.register (action, hotkey=hotkey)

        self.actionController.appendMenuItem (action.stringId, menu)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        menuItemId = self._getMenuItemId (action.stringId)
        toolid = self._getToolItemId (action.stringId)

        self.actionController.enableTools (action.stringId, False)
        self.assertFalse (toolbar.GetToolEnabled (toolid))
        self.assertFalse (menu.IsEnabled (menuItemId))

        self.actionController.enableTools (action.stringId, True)
        self.assertTrue (toolbar.GetToolEnabled (toolid))
        self.assertTrue (menu.IsEnabled (menuItemId))


    def testDisableToolsNone (self):
        action = TestAction()
        hotkey = HotKey ("T", ctrl=True)

        self.actionController.register (action, hotkey=hotkey)
        self.actionController.enableTools (action.stringId, False)


    def testGetActions1 (self):
        action1 = TestAction()
        action2 = TestCheckAction()

        self.actionController.register (action1)
        self.actionController.register (action2)

        self.assertEqual (self.actionController.getAction(action1.stringId), action1)
        self.assertEqual (self.actionController.getAction(action2.stringId), action2)


    def testGetActions2 (self):
        action1 = TestAction()
        action2 = TestCheckAction()
        self.actionController.register (action1)

        self.assertRaises (KeyError, self.actionController.getAction, action2.stringId)


    def testHotKeyLoadConfig (self):
        action = TestAction()
        hotKeyFromConfig = HotKey ("F11")
        HotKeyOption (Application.config, self.actionController.configSection, action.stringId, None).value = hotKeyFromConfig

        self.actionController.register (action, HotKey ("F12", ctrl=True))

        self.assertEqual (self.actionController.getHotKey (action.stringId).key, "F11")
        self.assertFalse (self.actionController.getHotKey (action.stringId).ctrl)
        self.assertFalse (self.actionController.getHotKey (action.stringId).shift)
        self.assertFalse (self.actionController.getHotKey (action.stringId).alt)


    def testHotKeySaveConfig1 (self):
        action = TestAction()
        hotkey = HotKey ("F11", ctrl=True)

        self.actionController.register (action, hotkey)
        self.actionController.saveHotKeys()

        otherActionController = ActionController (self.wnd, Application.config)
        otherActionController.register (action)

        self.assertEqual (otherActionController.getHotKey (action.stringId).key, "F11")
        self.assertTrue (otherActionController.getHotKey (action.stringId).ctrl)
        self.assertFalse (otherActionController.getHotKey (action.stringId).shift)
        self.assertFalse (otherActionController.getHotKey (action.stringId).alt)


    def testHotKeySaveConfig2 (self):
        action = TestAction()
        hotkey = HotKey ("F11", ctrl=True)

        self.actionController.register (action, hotkey)
        self.actionController.saveHotKeys()

        otherActionController = ActionController (self.wnd, Application.config)
        otherActionController.register (action, HotKey ("F1", shift=True))

        self.assertEqual (otherActionController.getHotKey (action.stringId).key, "F11")
        self.assertTrue (otherActionController.getHotKey (action.stringId).ctrl)
        self.assertFalse (otherActionController.getHotKey (action.stringId).shift)
        self.assertFalse (otherActionController.getHotKey (action.stringId).alt)


    def testHotKeySaveConfig3 (self):
        action = TestAction()

        self.actionController.register (action)
        self.actionController.saveHotKeys()

        otherActionController = ActionController (self.wnd, Application.config)
        otherActionController.register (action)

        self.assertEqual (otherActionController.getHotKey (action.stringId).key, "")
        self.assertFalse (otherActionController.getHotKey (action.stringId).ctrl)
        self.assertFalse (otherActionController.getHotKey (action.stringId).shift)
        self.assertFalse (otherActionController.getHotKey (action.stringId).alt)


    def testSetHotKey (self):
        action = TestAction()
        self.actionController.register (action, None)

        hotkey = HotKey ("F11", ctrl=True)
        self.actionController.setHotKey (action.stringId, hotkey)
        self.assertEqual (self.actionController.getHotKey (action.stringId), hotkey)


    def testChangeHotkeyGui (self):
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        hotkey = HotKey ("F11", ctrl=True)

        action = TestAction()
        self.actionController.register (action, None)

        self.actionController.appendMenuItem (action.stringId, menu)
        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.actionController.setHotKey (action.stringId, hotkey)

        self.assertEqual (self._getToolItemLabel (toolbar, action.stringId),
                          u"{} ({})".format (action.title, "Ctrl+F11"))

        self.assertEqual (self._getMenuItem(action.stringId).GetItemLabel(),
                          u"{}\t{}".format (action.title, "Ctrl+F11"))


    def testChangeHotkeyGuiMenu (self):
        menu = self.wnd.mainMenu.fileMenu

        hotkey = HotKey ("F11", ctrl=True)

        action = TestAction()
        self.actionController.register (action, None)

        self.actionController.appendMenuItem (action.stringId, menu)

        self.actionController.setHotKey (action.stringId, hotkey)

        self.assertEqual (self._getMenuItem(action.stringId).GetItemLabel(),
                          u"{}\t{}".format (action.title, "Ctrl+F11"))


    def testChangeHotkeyToolbar (self):
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        hotkey = HotKey ("F11", ctrl=True)

        action = TestAction()
        self.actionController.register (action, None)

        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.actionController.setHotKey (action.stringId, hotkey)

        self.assertEqual (self._getToolItemLabel (toolbar, action.stringId),
                          u"{} ({})".format (action.title, "Ctrl+F11"))


    def testDelayChangeHotkeyToolbar (self):
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        hotkey = HotKey ("F11", ctrl=True)

        action = TestAction()
        self.actionController.register (action, HotKey ("F11"))

        self.actionController.appendToolbarButton (action.stringId,
                                                   toolbar,
                                                   image)

        self.actionController.setHotKey (action.stringId, hotkey, False)

        self.assertEqual (self._getToolItemLabel (toolbar, action.stringId),
                          u"{} ({})".format (action.title, "F11"))

        otherActionController = ActionController (self.wnd, Application.config)
        otherActionController.register (action, None)

        self.assertEqual (otherActionController.getHotKey (action.stringId),
                          hotkey)


    def testChangeHotkeyGuiChecked1 (self):
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        hotkey = HotKey ("F11", ctrl=True)

        action = TestCheckAction()
        self.actionController.register (action, None)

        self.actionController.appendMenuCheckItem (action.stringId, menu)
        self.actionController.appendToolbarCheckButton (action.stringId,
                                                        toolbar,
                                                        image)

        self.actionController.setHotKey (action.stringId, hotkey)

        self.assertEqual (self._getToolItemLabel (toolbar, action.stringId),
                          u"{} ({})".format (action.title, "Ctrl+F11"))

        self.assertEqual (self._getMenuItem(action.stringId).GetItemLabel(),
                          u"{}\t{}".format (action.title, "Ctrl+F11"))


    def testChangeHotkeyGuiChecked2 (self):
        menu = self.wnd.mainMenu.fileMenu
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        image = "../test/images/save.png"

        hotkey = HotKey ("F11", ctrl=True)

        action = TestCheckAction()
        self.actionController.register (action, None)

        self.actionController.appendMenuCheckItem (action.stringId, menu)
        self.actionController.appendToolbarCheckButton (action.stringId,
                                                        toolbar,
                                                        image)

        menuItem = self._getMenuItem (action.stringId)
        toolItem = self._getToolItem (toolbar, action.stringId)

        self.actionController.setHotKey (action.stringId, hotkey)
        self.actionController.check (action.stringId, True)

        self.assertTrue (menuItem.IsChecked())
        self.assertTrue (toolItem.GetState())


    def _assertMenuItemExists (self, menu, title, hotkey):
        """
        Проверить, что в меню есть элемент с заголовком (title + '\t' + hotkey)
        """
        menuItemId = menu.FindItem (title)
        self.assertNotEqual (menuItemId, wx.NOT_FOUND)

        menuItem = menu.FindItemById (menuItemId)

        if hotkey is not None:
            self.assertEqual (menuItem.GetItemLabel(), title + "\t" + HotKeyParser.toString (hotkey))
        else:
            self.assertEqual (menuItem.GetItemLabel(), title)


    def _emulateMenuClick (self, menuItemId):
        """
        Эмуляция события выбора пункта меню
        """
        event = wx.CommandEvent (wx.wxEVT_COMMAND_MENU_SELECTED, menuItemId)
        self.wnd.ProcessEvent (event)


    def _emulateButtonClick (self, toolitemId):
        """
        Эмуляция события выбора пункта меню
        """
        event = wx.CommandEvent (wx.wxEVT_COMMAND_TOOL_CLICKED, toolitemId)
        self.wnd.ProcessEvent (event)


    def _emulateCheckButtonClick (self, toolitemId):
        """
        Эмуляция события выбора пункта меню
        """
        toolbar = self.wnd.toolbars[self.wnd.PLUGINS_TOOLBAR_STR]
        toolitem = toolbar.FindTool (toolitemId)
        newState = not toolitem.GetState()
        toolbar.ToggleTool (toolitemId, newState)

        event = wx.CommandEvent (wx.wxEVT_COMMAND_TOOL_CLICKED, toolitemId)
        event.SetInt (newState)
        self.wnd.ProcessEvent (event)


    def _getMenuItemId (self, strid):
        result = None

        actionInfo = self.actionController.getActionInfo(strid)
        if actionInfo is not None:
            result = actionInfo.menuItem.GetId()

        return result


    def _getMenuItem (self, strid):
        result = None

        actionInfo = self.actionController.getActionInfo(strid)
        if actionInfo is not None:
            result = actionInfo.menuItem

        return result


    def _getToolItemId (self, strid):
        """
        Получить идентификатор кнопки с панели инструментов
        """
        result = None

        actionInfo = self.actionController.getActionInfo(strid)
        if actionInfo is not None:
            result = actionInfo.toolItemId

        return result


    def _getToolItemLabel (self, toolbar, strid):
        result = None

        item = self._getToolItem (toolbar, strid)

        if item is not None:
            result = item.GetShortHelp()

        return result


    def _getToolItem (self, toolbar, strid):
        result = None

        itemId = self._getToolItemId (strid)
        if itemId is not None:
            result = toolbar.FindTool (itemId)

        return result

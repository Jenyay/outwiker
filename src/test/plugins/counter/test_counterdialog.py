# -*- coding: utf-8 -*-

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUITest


class CounterDialogTest(BaseOutWikerGUITest):
    """
    Тесты диалога для плагина Counter
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.filesPath = "../test/samplefiles/"
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        dirlist = ["../plugins/counter"]

        self._loader = PluginsLoader(self.application)
        self._loader.load(dirlist)

        from counter.insertdialog import InsertDialog
        self._dlg = InsertDialog(self.application.mainWindow)
        Tester.dialogTester.clear()
        Tester.dialogTester.appendOk()

        self.testPage = self.wikiroot["Страница 1"]

    def tearDown(self):
        self.application.wikiroot = None
        self._dlg.Destroy()
        self._loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testDefault(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(
            self._dlg,
            self.application.config,
            self.testPage)

        result = controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(result, wx.ID_OK)
        self.assertEqual(self._dlg.counterName, "")
        self.assertEqual(self._dlg.parentName, "")
        self.assertEqual(self._dlg.separator, ".")
        self.assertEqual(self._dlg.reset, False)
        self.assertEqual(self._dlg.start, 1)
        self.assertEqual(self._dlg.step, 1)
        self.assertEqual(self._dlg.hide, False)
        self.assertEqual(self._dlg.countersList, [""])

        self.assertEqual(text, '(:counter:)')

    def testDestroy(self):
        self.application.wikiroot = None
        self._loader.clear()

    def testSetEmptyName_01(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.counterName = ""

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testSetEmptyName_02(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.counterName = "    "

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testSetName(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.counterName = "Имя счетчика"

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter name="Имя счетчика":)')

    def testSetParentEmptyName_01(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.parentName = ""

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testSetParentEmptyName_02(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.parentName = "     "

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testSetParentName(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.parentName = "Имя счетчика"

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter parent="Имя счетчика":)')

    def testSetSeparatorDefault(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.separator = "."

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testSetSeparatorWithoutParent(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.separator = ":"

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testSetSeparatorWithParent_01(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.separator = ":"
        self._dlg.parentName = "Родительский счетчик"

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(
            text,
            '(:counter parent="Родительский счетчик" separator=":":)')

    def testNotReset_01(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.reset = False
        self._dlg.start = 0

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testNotReset_02(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.reset = False
        self._dlg.start = 100

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testReset_01(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.reset = True
        self._dlg.start = 0

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter start=0:)')

    def testReset_02(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.reset = True
        self._dlg.start = -10

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter start=-10:)')

    def testReset_03(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.reset = True
        self._dlg.start = 1

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter start=1:)')

    def testReset_04(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.reset = True
        self._dlg.start = 10

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter start=10:)')

    def testStep_01(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.step = 1
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testStep_02(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.step = 0
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter step=0:)')

    def testStep_03(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.step = -10
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter step=-10:)')

    def testStep_04(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.step = 10
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter step=10:)')

    def testHide_01(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.hide = False
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter:)')

    def testHide_02(self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController(self._dlg,
                                            self.application.config,
                                            self.testPage)

        self._dlg.hide = True
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual(text, '(:counter hide:)')

    def testCountersList_01(self):
        self.testPage.content = '''(:counter:)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController(self._dlg,
                               self.application.config,
                               self.testPage)

        self.assertEqual(self._dlg.countersList, [""])

    def testCountersList_02(self):
        self.testPage.content = '''(:counter name="Счетчик":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController(self._dlg,
                               self.application.config,
                               self.testPage)

        self.assertEqual(self._dlg.countersList, ["", "Счетчик"])

    def testCountersList_03(self):
        self.testPage.content = '''(:counter name="Счетчик":)(:counter name="Счетчик":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController(self._dlg, self.application.config, self.testPage)

        self.assertEqual(self._dlg.countersList, ["", "Счетчик"])

    def testCountersList_04(self):
        self.testPage.content = '''(:counter name="Счетчик":)(:counter name="Абырвалг   ":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController(self._dlg, self.application.config, self.testPage)

        self.assertEqual(self._dlg.countersList, ["", "Абырвалг", "Счетчик"])

    def testCountersList_05(self):
        self.testPage.content = '''(:counter name="Счетчик":)(:counter name='Абырвалг':)(:counter name="":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController(self._dlg, self.application.config, self.testPage)

        self.assertEqual(self._dlg.countersList, ["", "Абырвалг", "Счетчик"])

    def testCountersList_06(self):
        self.testPage.content = '''(:counter name="Счетчик":)(:counter name=Абырвалг:)(:counter name="":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController(self._dlg, self.application.config, self.testPage)

        self.assertEqual(self._dlg.countersList, ["", "Абырвалг", "Счетчик"])

# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUIMixin


class InsertDiagramTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        dirlist = ["../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        from diagrammer.gui.insertdiagramdialog import (
            InsertDiagramDialog,
            InsertDiagramController
        )

        self._dlg = InsertDiagramDialog(None)
        self._controller = InsertDiagramController(self._dlg)
        Tester.dialogTester.clear()

    def tearDown(self):
        self._dlg.Destroy()
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testDefault(self):
        Tester.dialogTester.appendOk()

        begin, end = self._controller.getResult()

        self.assertEqual(begin, "(:diagram:)\n")
        self.assertEqual(end, "\n(:diagramend:)")

    def testShape_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.setShapeSelection(0)

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = actor;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n(:diagramend:)")

    def testShape_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.setShapeSelection(1)

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = beginpoint;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n(:diagramend:)")

    def testShape_03(self):
        Tester.dialogTester.appendOk()

        # Значение по умолчанию
        self._dlg.setShapeSelection(2)

        begin, end = self._controller.getResult()

        self.assertEqual(begin, "(:diagram:)\n")
        self.assertEqual(end, "\n(:diagramend:)")

    def testNodeColor_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = "white"

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_node_color = "white";
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testNodeColor_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBackColorChanged = False
        self._dlg.backColor = "black"

        begin, end = self._controller.getResult()

        self.assertEqual(begin, '(:diagram:)\n')
        self.assertEqual(end, '\n(:diagramend:)')

    def testNodeColor_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = "#AAAAAA"

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_node_color = "#AAAAAA";
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testNodeColor_04(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = "#AAAAAA"
        self._dlg.setShapeSelection(0)

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = actor;
default_node_color = "#AAAAAA";
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testTextColor_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = "white"

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_textcolor = "white";
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testTextColor_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isTextColorChanged = False
        self._dlg.textColor = "black"

        begin, end = self._controller.getResult()

        self.assertEqual(begin, '(:diagram:)\n')
        self.assertEqual(end, '\n(:diagramend:)')

    def testTextColor_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = "#AAAAAA"

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_textcolor = "#AAAAAA";
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testTextColor_04(self):
        Tester.dialogTester.appendOk()
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = "#AAAAAA"
        self._dlg.setShapeSelection(0)

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = actor;
default_textcolor = "#AAAAAA";
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testFontSize_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isFontSizeChanged = True
        self._dlg.fontSize = 20

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_fontsize = 20;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testFontSize_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isFontSizeChanged = False
        self._dlg.fontSize = 20

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testFontSize_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.setShapeSelection(0)
        self._dlg.isFontSizeChanged = True
        self._dlg.fontSize = 20

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = actor;
default_fontsize = 20;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testWidth_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isWidthChanged = True
        self._dlg.width = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
node_width = 200;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testWidth_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isWidthChanged = False
        self._dlg.width = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testWidth_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.setShapeSelection(0)
        self._dlg.isWidthChanged = True
        self._dlg.width = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = actor;
node_width = 200;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testHeight_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isHeightChanged = True
        self._dlg.height = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
node_height = 200;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testHeight_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isHeightChanged = False
        self._dlg.height = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testHeight_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.setShapeSelection(0)
        self._dlg.isHeightChanged = True
        self._dlg.height = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = actor;
node_height = 200;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testOrientation_01(self):
        self._dlg.orientationIndex = 0

        Tester.dialogTester.appendOk()

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testOrientation_02(self):
        self._dlg.orientationIndex = 1

        Tester.dialogTester.appendOk()

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
orientation = portrait;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testOrientation_03(self):
        self._dlg.orientationIndex = 1
        self._dlg.setShapeSelection(0)

        Tester.dialogTester.appendOk()

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
orientation = portrait;
default_shape = actor;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testSpanWidth_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isSpanWidthChanged = True
        self._dlg.spanWidth = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
span_width = 200;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testSpanWidth_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isSpanWidthChanged = False
        self._dlg.spanWidth = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testSpanWidth_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.setShapeSelection(0)
        self._dlg.isSpanWidthChanged = True
        self._dlg.spanWidth = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = actor;
span_width = 200;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testSpanHeight_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isSpanHeightChanged = True
        self._dlg.spanHeight = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
span_height = 200;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testSpanHeight_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isSpanHeightChanged = False
        self._dlg.spanHeight = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

    def testSpanHeight_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.setShapeSelection(0)
        self._dlg.isSpanHeightChanged = True
        self._dlg.spanHeight = 200

        begin, end = self._controller.getResult()

        valid_begin = '''(:diagram:)
default_shape = actor;
span_height = 200;
'''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, '\n(:diagramend:)')

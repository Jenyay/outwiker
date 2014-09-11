# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.gui.tester import Tester


class InsertNodeTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.plugin = self.loader[u"Diagrammer"]

        self._dlg = self.plugin.InsertNodeDialog(None)
        self._controller = self.plugin.InsertNodeController (self._dlg)
        Tester.dialogTester.clear()


    def tearDown(self):
        self._dlg.Destroy()
        self.loader.clear()


    def testDestroy (self):
        Application.wikiroot = None
        self.loader.clear()


    def testName_01 (self):

        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        result = self._controller.getResult ()

        self.assertEqual (result, u"Абырвалг")


    def testName_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг 111"

        result = self._controller.getResult ()

        self.assertEqual (result, u'"Абырвалг 111"')


    def testShapeSelection_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.setShapeSelection (0)

        result = self._controller.getResult ()

        self.assertEqual (result, u"Абырвалг")


    def testShapeSelection_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.setShapeSelection (1)

        result = self._controller.getResult ()

        self.assertEqual (result, u"Абырвалг [shape = actor];")


    def testShapeSelection_03 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.setShapeSelection (10)

        result = self._controller.getResult ()

        self.assertEqual (result, u"Абырвалг [shape = flowchart.database];")


    def testBorderStyle_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.setStyleIndex (0)

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг")


    def testBorderStyle_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.setStyleIndex (1)

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_03 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.setStyleIndex (2)

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = dotted];")


    def testBorderStyle_04 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.style = u""

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг")


    def testBorderStyle_05 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.style = u"solid"

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_06 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.style = u"Solid"

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_07 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.style = u" Solid "

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_08 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.style = u"1,2,3"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_09 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.style = u"1, 2, 3"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_10 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.style = u" 1, 2, 3 "

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_11 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.style = u'"1,2,3"'

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_12 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"

        self._dlg.setShapeSelection (1)
        self._dlg.style = u"dotted"

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг [shape = actor, style = dotted];")


    def testStacked_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.stacked = True

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг [stacked];")


    def testStacked_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.stacked = True
        self._dlg.setShapeSelection (1)

        result = self._controller.getResult ()
        self.assertEqual (result, u"Абырвалг [shape = actor, stacked];")


    def testLabel_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.label = u"Превед"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [label = "Превед"];')


    def testLabel_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.setShapeSelection (1)
        self._dlg.label = u"Превед"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [shape = actor, label = "Превед"];')


    def testLabel_03 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.label = u"Абырвалг"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг')


    def testColor_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = u"white"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [color = "white"];')


    def testColor_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = u"#AAAAAA"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [color = "#AAAAAA"];')


    def testColor_03 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isBackColorChanged = False
        self._dlg.backColor = u"#AAAAAA"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг')


    def testColor_04 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.setShapeSelection (1)
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = u"#AAAAAA"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [shape = actor, color = "#AAAAAA"];')


    def testTextColor_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = u"black"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [textcolor = "black"];')


    def testTextColor_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = u"#AAAAAA"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [textcolor = "#AAAAAA"];')


    def testTextColor_03 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isTextColorChanged = False
        self._dlg.textColor = u"#AAAAAA"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг')


    def testTextColor_04 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.setShapeSelection (1)
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = u"#AAAAAA"

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [shape = actor, textcolor = "#AAAAAA"];')


    def testFontSize_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isFontSizeChanged = True
        self._dlg.fontSize = 20

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [fontsize = 20];')


    def testFontSize_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isFontSizeChanged = False
        self._dlg.fontSize = 20

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг')


    def testFontSize_03 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.setShapeSelection (1)
        self._dlg.isFontSizeChanged = True
        self._dlg.fontSize = 20

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [shape = actor, fontsize = 20];')


    def testWidth_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isWidthChanged = True
        self._dlg.width = 200

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [width = 200];')


    def testWidth_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isWidthChanged = False
        self._dlg.width = 200

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг')


    def testWidth_03 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.setShapeSelection (1)
        self._dlg.isWidthChanged = True
        self._dlg.width = 200

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [shape = actor, width = 200];')


    def testHeight_01 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isHeightChanged = True
        self._dlg.height = 200

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [height = 200];')


    def testHeight_02 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.isHeightChanged = False
        self._dlg.height = 200

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг')


    def testHeight_03 (self):
        Tester.dialogTester.appendOk()
        self._dlg.name = u"Абырвалг"
        self._dlg.setShapeSelection (1)
        self._dlg.isHeightChanged = True
        self._dlg.height = 200

        result = self._controller.getResult ()
        self.assertEqual (result, u'Абырвалг [shape = actor, height = 200];')

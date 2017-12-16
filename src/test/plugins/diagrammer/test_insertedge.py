# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.gui.tester import Tester


class InsertEdgeTest (unittest.TestCase):
    def setUp(self):
        dirlist = ["../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        from diagrammer.gui.insertedgedialog import InsertEdgeDialog

        self._dlg = InsertEdgeDialog (None)
        Tester.dialogTester.clear()


    def tearDown(self):
        self.loader.clear()
        self._dlg.Destroy()


    def testArrows_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerNone (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"

        result = controller.getResult ()

        self.assertEqual (result, "А -- Б")


    def testArrows_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerLeft (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"

        result = controller.getResult ()

        self.assertEqual (result, "А <- Б")


    def testArrows_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"

        result = controller.getResult ()

        self.assertEqual (result, "А -> Б")


    def testArrows_04 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerBoth (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"

        result = controller.getResult ()

        self.assertEqual (result, "А <-> Б")


    def testEmptyNames_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerBoth (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = ""
        self._dlg.secondName = ""

        result = controller.getResult ()

        self.assertIn ("1", result)
        self.assertIn ("2", result)


    def testEmptyNames_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerBoth (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = ""

        result = controller.getResult ()

        self.assertNotIn ("1", result)
        self.assertIn ("А", result)
        self.assertIn ("2", result)


    def testEmptyNames_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerBoth (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = ""
        self._dlg.secondName = "Б"

        result = controller.getResult ()

        self.assertIn ("1", result)
        self.assertNotIn ("2", result)
        self.assertIn ("Б", result)


    def testLabel_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.label = "Абырвалг"

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [label = "Абырвалг"]')


    def testStyleLine_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setStyleIndex (0)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б')


    def testStyleLine_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setStyleIndex (1)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [style = solid]')


    def testStyleLine_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setStyleIndex (2)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [style = dotted]')


    def testStyleLine_04 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [style = dashed]')


    def testStyleLine_05 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.label = "Абырвалг"
        self._dlg.setStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [label = "Абырвалг", style = dashed]')


    def testStyleArrow_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setArrowStyleIndex (0)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б')


    def testStyleArrow_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setArrowStyleIndex (1)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [hstyle = generalization]')


    def testStyleArrow_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setArrowStyleIndex (2)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [hstyle = composition]')


    def testStyleArrow_04 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setArrowStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [hstyle = aggregation]')


    def testStyleArrow_05 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.setStyleIndex (3)
        self._dlg.setArrowStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [style = dashed, hstyle = aggregation]')


    def testLineColor_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isLineColorChanged = True
        self._dlg.lineColor = "yellow"

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [color = "yellow"]')


    def testLineColor_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isLineColorChanged = False
        self._dlg.lineColor = "yellow"

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б')


    def testLineColor_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isLineColorChanged = True
        self._dlg.lineColor = "#AAAAAA"

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [color = "#AAAAAA"]')


    def testLineColor_04 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isLineColorChanged = True
        self._dlg.lineColor = "#AAAAAA"
        self._dlg.setArrowStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [hstyle = aggregation, color = "#AAAAAA"]')


    def testFontSize_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isFontSizeChanged = True
        self._dlg.fontSize = 11

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [fontsize = 11]')


    def testFontSize_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isFontSizeChanged = False
        self._dlg.fontSize = 15

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б')


    def testFontSize_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isFontSizeChanged = True
        self._dlg.fontSize = 11
        self._dlg.label = "Абырвалг"

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [label = "Абырвалг", fontsize = 11]')


    def testTextColor_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = "yellow"

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [textcolor = "yellow"]')


    def testTextColor_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isTextColorChanged = False
        self._dlg.textColor = "yellow"

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б')


    def testTextColor_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = "#AAAAAA"

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [textcolor = "#AAAAAA"]')


    def testTextColor_04 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = "#AAAAAA"
        self._dlg.setArrowStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [hstyle = aggregation, textcolor = "#AAAAAA"]')


    def testThick_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.thick = True

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [thick]')


    def testThick_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.thick = False

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б')


    def testThick_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.thick = True
        self._dlg.setStyleIndex (1)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [style = solid, thick]')


    def testFolded_01 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.folded = True

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [folded]')


    def testFolded_02 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.folded = False

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б')


    def testFolded_03 (self):
        import diagrammer.gui.insertedgedialog

        controller = diagrammer.gui.insertedgedialog.InsertEdgeControllerRight (self._dlg)

        Tester.dialogTester.appendOk()
        self._dlg.firstName = "А"
        self._dlg.secondName = "Б"
        self._dlg.folded = True
        self._dlg.setStyleIndex (1)

        result = controller.getResult ()

        self.assertEqual (result, 'А -> Б [style = solid, folded]')

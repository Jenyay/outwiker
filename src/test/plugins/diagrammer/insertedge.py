# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class InsertEdgeTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.plugin = self.loader[u"Diagrammer"]


    def tearDown(self):
        self.loader.clear()


    def testArrows_01 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerNone (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"

        result = controller.getResult ()

        self.assertEqual (result, u"А -- Б")


    def testArrows_02 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerLeft (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"

        result = controller.getResult ()

        self.assertEqual (result, u"А <- Б")


    def testArrows_03 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"

        result = controller.getResult ()

        self.assertEqual (result, u"А -> Б")


    def testArrows_04 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerBoth (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"

        result = controller.getResult ()

        self.assertEqual (result, u"А <-> Б")


    def testEmptyNames_01 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerBoth (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u""
        dlg.secondName = u""

        result = controller.getResult ()

        self.assertIn (u"1", result)
        self.assertIn (u"2", result)


    def testEmptyNames_02 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerBoth (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u""

        result = controller.getResult ()

        self.assertNotIn (u"1", result)
        self.assertIn (u"А", result)
        self.assertIn (u"2", result)


    def testEmptyNames_03 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerBoth (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u""
        dlg.secondName = u"Б"

        result = controller.getResult ()

        self.assertIn (u"1", result)
        self.assertNotIn (u"2", result)
        self.assertIn (u"Б", result)


    def testLabel_01 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.label = u"Абырвалг"

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [label = "Абырвалг"]')


    def testStyleLine_01 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setStyleIndex (0)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б')


    def testStyleLine_02 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setStyleIndex (1)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [style = solid]')


    def testStyleLine_03 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setStyleIndex (2)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [style = dotted]')


    def testStyleLine_04 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [style = dashed]')


    def testStyleLine_05 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.label = u"Абырвалг"
        dlg.setStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [label = "Абырвалг", style = dashed]')


    def testStyleArrow_01 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setArrowStyleIndex (0)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б')


    def testStyleArrow_02 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setArrowStyleIndex (1)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [hstyle = generalization]')


    def testStyleArrow_03 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setArrowStyleIndex (2)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [hstyle = composition]')


    def testStyleArrow_04 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setArrowStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [hstyle = aggregation]')


    def testStyleArrow_05 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.setStyleIndex (3)
        dlg.setArrowStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [style = dashed, hstyle = aggregation]')


    def testLineColor_01 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.isLineColorChanged = True
        dlg.lineColor = u"yellow"

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [color = "yellow"]')


    def testLineColor_02 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.isLineColorChanged = False
        dlg.lineColor = u"yellow"

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б')


    def testLineColor_03 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.isLineColorChanged = True
        dlg.lineColor = u"#AAAAAA"

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [color = "#AAAAAA"]')


    def testLineColor_04 (self):
        dlg = self.plugin.InsertEdgeDialog(None)
        controller = self.plugin.InsertEdgeControllerRight (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.firstName = u"А"
        dlg.secondName = u"Б"
        dlg.isLineColorChanged = True
        dlg.lineColor = u"#AAAAAA"
        dlg.setArrowStyleIndex (3)

        result = controller.getResult ()

        self.assertEqual (result, u'А -> Б [hstyle = aggregation, color = "#AAAAAA"]')

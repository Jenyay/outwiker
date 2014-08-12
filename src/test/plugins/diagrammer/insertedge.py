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

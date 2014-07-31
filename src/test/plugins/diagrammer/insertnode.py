# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class InsertNodeTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.plugin = self.loader[u"Diagrammer"]


    def tearDown(self):
        self.loader.clear()


    def testDefault (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        result = controller.getResult ()

        self.assertEqual (result, u"Абырвалг")


    def testShapeSelection_01 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.setShapeSelection (0)

        result = controller.getResult ()

        self.assertEqual (result, u"Абырвалг")


    def testShapeSelection_02 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.setShapeSelection (1)

        result = controller.getResult ()

        self.assertEqual (result, u"Абырвалг [shape = actor];")


    def testShapeSelection_03 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.setShapeSelection (10)

        result = controller.getResult ()

        self.assertEqual (result, u"Абырвалг [shape = flowchart.database];")

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


    def testBorderStyle_01 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setBorderStyleIndex = 0

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг")


    def testBorderStyle_02 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setBorderStyleIndex (1)

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_03 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setBorderStyleIndex (2)

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = dotted];")


    def testBorderStyle_04 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u""

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг")


    def testBorderStyle_05 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u"solid"

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_06 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u"Solid"

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_07 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u" Solid "

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_08 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u"1,2,3"

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_09 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u"1, 2, 3"

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_10 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u" 1, 2, 3 "

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_11 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u'"1,2,3"'

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_12 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setShapeSelection (1)
        dlg.borderStyle = u"dotted"

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [shape = actor, style = dotted];")

# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class InsertDiagramTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.plugin = self.loader[u"Diagrammer"]


    def tearDown(self):
        self.loader.clear()


    def testDefault (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)

        begin, end = controller.getResult ()

        self.assertEqual (begin, u"(:diagram:)\n")
        self.assertEqual (end, u"\n(:diagramend:)")


    def testShape_01 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.setShapeSelection (0)

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_shape = actor;
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n(:diagramend:)")


    def testShape_02 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.setShapeSelection (1)

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_shape = beginpoint;
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n(:diagramend:)")


    def testShape_03 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)

        # Значение по умолчанию
        dlg.setShapeSelection (2)

        begin, end = controller.getResult ()

        self.assertEqual (begin, u"(:diagram:)\n")
        self.assertEqual (end, u"\n(:diagramend:)")


    def testNodeColor_01 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBackColorChanged = True
        dlg.backColor = u"white"

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_node_color = "white";
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testNodeColor_02 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBackColorChanged = False
        dlg.backColor = u"black"

        begin, end = controller.getResult ()

        self.assertEqual (begin, u'(:diagram:)\n')
        self.assertEqual (end, u'\n(:diagramend:)')


    def testNodeColor_03 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBackColorChanged = True
        dlg.backColor = u"#AAAAAA"

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_node_color = "#AAAAAA";
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testNodeColor_04 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBackColorChanged = True
        dlg.backColor = u"#AAAAAA"
        dlg.setShapeSelection (0)

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_shape = actor;
default_node_color = "#AAAAAA";
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testTextColor_01 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isTextColorChanged = True
        dlg.textColor = u"white"

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_textcolor = "white";
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testTextColor_02 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isTextColorChanged = False
        dlg.textColor = u"black"

        begin, end = controller.getResult ()

        self.assertEqual (begin, u'(:diagram:)\n')
        self.assertEqual (end, u'\n(:diagramend:)')


    def testTextColor_03 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isTextColorChanged = True
        dlg.textColor = u"#AAAAAA"

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_textcolor = "#AAAAAA";
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testTextColor_04 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isTextColorChanged = True
        dlg.textColor = u"#AAAAAA"
        dlg.setShapeSelection (0)

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_shape = actor;
default_textcolor = "#AAAAAA";
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testFontSize_01 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isFontSizeChanged = True
        dlg.fontSize = 20

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_fontsize = 20;
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testFontSize_02 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isFontSizeChanged = False
        dlg.fontSize = 20

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testFontSize_03 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.setShapeSelection (0)
        dlg.isFontSizeChanged = True
        dlg.fontSize = 20

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_shape = actor;
default_fontsize = 20;
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testWidth_01 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isWidthChanged = True
        dlg.width = 200

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
node_width = 200;
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testWidth_02 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isWidthChanged = False
        dlg.width = 200

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testWidth_03 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.setShapeSelection (0)
        dlg.isWidthChanged = True
        dlg.width = 200

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_shape = actor;
node_width = 200;
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testHeight_01 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isHeightChanged = True
        dlg.height = 200

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
node_height = 200;
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testHeight_02 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isHeightChanged = False
        dlg.height = 200

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')


    def testHeight_03 (self):
        dlg = self.plugin.InsertDiagramDialog(None)
        controller = self.plugin.InsertDiagramController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.setShapeSelection (0)
        dlg.isHeightChanged = True
        dlg.height = 200

        begin, end = controller.getResult ()

        valid_begin = u'''(:diagram:)
default_shape = actor;
node_height = 200;
'''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u'\n(:diagramend:)')

# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class InsertGroupTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.plugin = self.loader[u"Diagrammer"]

        self._dlg = self.plugin.InsertGroupDialog(None)
        self._controller = self.plugin.InsertGroupController (self._dlg)


    def tearDown(self):
        self.loader.clear()
        self._dlg.Destroy()


    def testDefault (self):
        self._dlg.SetModalResult (wx.ID_OK)

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testName_01 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.name = u"Абырвалг"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group Абырвалг {
    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testBackColor_01 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = u"blue"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    color = "blue";

    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testBackColor_02 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBackColorChanged = False
        self._dlg.backColor = u"blue"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testBackColor_03 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = u"#AAAAAA"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    color = "#AAAAAA";

    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testOrientation_01 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isOrientationChanged = True
        self._dlg.orientationIndex = 0

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    orientation = landscape;

    '''

        self.assertEqual (begin, valid_begin)


    def testOrientation_02 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isOrientationChanged = True
        self._dlg.orientationIndex = 1

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    orientation = portrait;

    '''

        self.assertEqual (begin, valid_begin)


    def testOrientation_03 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isOrientationChanged = False
        self._dlg.orientationIndex = 1

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)


    def testOrientation_04 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isOrientationChanged = True
        self._dlg.orientationIndex = 1
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = u"blue"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    color = "blue";
    orientation = portrait;

    '''

        self.assertEqual (begin, valid_begin)


    def testLabel_01 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.label = u"Абырвалг"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    label = "Абырвалг";

    '''

        self.assertEqual (begin, valid_begin)


    def testLabel_02 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.label = u""

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)


    def testTextColor_01 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = u"blue"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    textcolor = "blue";

    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testTextColor_02 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isTextColorChanged = False
        self._dlg.textColor = u"blue"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testTextColor_03 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = u"#AAAAAA"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    textcolor = "#AAAAAA";

    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testBorderShape_01 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 0

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    shape = box;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderShape_02 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    shape = line;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderShape_03 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = False
        self._dlg.borderShapeIndex = 1

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_01 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.setStyleIndex (1)

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = solid;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_02 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = False
        self._dlg.borderShapeIndex = 1

        self._dlg.setStyleIndex (1)

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_03 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 0

        self._dlg.setStyleIndex (1)

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    shape = box;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_04 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.setStyleIndex (2)

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = dotted;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_05 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.setStyleIndex (3)

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = dashed;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_06 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.style = u"1,2,3,4"

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = "1,2,3,4";

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_07 (self):
        self._dlg.SetModalResult (wx.ID_OK)
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.style = u" 1, 2, 3, 4 "

        begin, end = self._controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = "1,2,3,4";

    '''

        self.assertEqual (begin, valid_begin)

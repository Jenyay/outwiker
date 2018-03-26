# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.gui.tester import Tester


class InsertGroupTest(unittest.TestCase):
    def setUp(self):
        dirlist = ["../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        from diagrammer.gui.insertgroupdialog import (
            InsertGroupDialog,
            InsertGroupController
        )

        self._dlg = InsertGroupDialog(None)
        self._controller = InsertGroupController(self._dlg)
        Tester.dialogTester.clear()

    def tearDown(self):
        self.loader.clear()
        self._dlg.Destroy()

    def testDefault(self):
        Tester.dialogTester.appendOk()

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    '''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n}")

    def testName_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.name = "Абырвалг"

        begin, end = self._controller.getResult()

        valid_begin = '''group Абырвалг {
    '''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n}")

    def testBackColor_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = "blue"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    color = "blue";

    '''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n}")

    def testBackColor_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBackColorChanged = False
        self._dlg.backColor = "blue"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    '''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n}")

    def testBackColor_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = "#AAAAAA"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    color = "#AAAAAA";

    '''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n}")

    def testOrientation_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isOrientationChanged = True
        self._dlg.orientationIndex = 0

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    orientation = landscape;

    '''

        self.assertEqual(begin, valid_begin)

    def testOrientation_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isOrientationChanged = True
        self._dlg.orientationIndex = 1

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    orientation = portrait;

    '''

        self.assertEqual(begin, valid_begin)

    def testOrientation_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.isOrientationChanged = False
        self._dlg.orientationIndex = 1

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    '''

        self.assertEqual(begin, valid_begin)

    def testOrientation_04(self):
        Tester.dialogTester.appendOk()
        self._dlg.isOrientationChanged = True
        self._dlg.orientationIndex = 1
        self._dlg.isBackColorChanged = True
        self._dlg.backColor = "blue"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    color = "blue";
    orientation = portrait;

    '''

        self.assertEqual(begin, valid_begin)

    def testLabel_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.label = "Абырвалг"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    label = "Абырвалг";

    '''

        self.assertEqual(begin, valid_begin)

    def testLabel_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.label = ""

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    '''

        self.assertEqual(begin, valid_begin)

    def testTextColor_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = "blue"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    textcolor = "blue";

    '''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n}")

    def testTextColor_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isTextColorChanged = False
        self._dlg.textColor = "blue"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    '''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n}")

    def testTextColor_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.isTextColorChanged = True
        self._dlg.textColor = "#AAAAAA"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    textcolor = "#AAAAAA";

    '''

        self.assertEqual(begin, valid_begin)
        self.assertEqual(end, "\n}")

    def testBorderShape_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 0

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    shape = box;

    '''

        self.assertEqual(begin, valid_begin)

    def testBorderShape_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    shape = line;

    '''

        self.assertEqual(begin, valid_begin)

    def testBorderShape_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = False
        self._dlg.borderShapeIndex = 1

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    '''

        self.assertEqual(begin, valid_begin)

    def testBorderStyle_01(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.setStyleIndex(1)

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    shape = line;
    style = solid;

    '''

        self.assertEqual(begin, valid_begin)

    def testBorderStyle_02(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = False
        self._dlg.borderShapeIndex = 1

        self._dlg.setStyleIndex(1)

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    '''

        self.assertEqual(begin, valid_begin)

    def testBorderStyle_03(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 0

        self._dlg.setStyleIndex(1)

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    shape = box;

    '''

        self.assertEqual(begin, valid_begin)

    def testBorderStyle_04(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.setStyleIndex(2)

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    shape = line;
    style = dotted;

    '''

        self.assertEqual(begin, valid_begin)

    def testBorderStyle_05(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.setStyleIndex(3)

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    shape = line;
    style = dashed;

    '''

        self.assertEqual(begin, valid_begin)

    def testBorderStyle_06(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.style = "1,2,3,4"

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    shape = line;
    style = "1,2,3,4";

    '''

        self.assertEqual(begin, valid_begin)

    def testBorderStyle_07(self):
        Tester.dialogTester.appendOk()
        self._dlg.isBorderShapeChanged = True
        self._dlg.borderShapeIndex = 1

        self._dlg.style = " 1, 2, 3, 4 "

        begin, end = self._controller.getResult()

        valid_begin = '''group {
    shape = line;
    style = "1,2,3,4";

    '''

        self.assertEqual(begin, valid_begin)

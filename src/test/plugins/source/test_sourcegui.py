# -*- coding: utf-8 -*-

import os.path
import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.basetestcases import BaseOutWikerGUIMixin
from .sourcefakedialog import FakeInsertDialog


class SourceGuiPluginTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты интерфейса для плагина Source
    """

    def setUp(self):
        self.__pluginname = "Source"
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot,
                                                 "Страница 1",
                                                 [])

        dirlist = ["../plugins/source"]
        self._stylesCount = 29

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.config = self.loader[self.__pluginname].config
        self._clearConfig(self.config)

        from source.insertdialogcontroller import InsertDialogController
        self.dialog = FakeInsertDialog()
        self.controller = InsertDialogController(
            self.testPage, self.dialog, self.config)

    def tearDown(self):
        self._clearConfig(self.config)
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _clearConfig(self, config):
        self.application.config.remove_section(self.config.section)

    def testDialogController1(self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.dialog.SetReturnCode(wx.ID_CANCEL)
        result = self.controller.showDialog()

        self.assertEqual(result, wx.ID_CANCEL)

    def testDialogController2(self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.dialog.SetReturnCode(wx.ID_OK)
        result = self.controller.showDialog()

        self.assertEqual(result, wx.ID_OK)

    def testDialogControllerResult1(self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = ["python", "cpp", "haskell", "text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode(wx.ID_OK)
        self.controller.showDialog()

        self.dialog.tabWidthSpin.SetValue(4)
        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="text" tabwidth="4":)\n', '\n(:sourceend:)'))

    def testDialogControllerResult2(self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.defaultLanguage.value = "python"

        self.dialog.SetReturnCode(wx.ID_OK)
        self.controller.showDialog()

        self.dialog.tabWidthSpin.SetValue(8)
        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python" tabwidth="8":)\n', '\n(:sourceend:)'))

    def testDialogControllerResult3(self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = ["python", "cpp", "haskell", "text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode(wx.ID_OK)
        self.controller.showDialog()

        self.dialog.tabWidthSpin.SetValue(4)
        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="text" tabwidth="4":)\n', '\n(:sourceend:)'))

    def testDialogControllerResult4(self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = ["python", "cpp", "haskell", "text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode(wx.ID_OK)
        self.controller.showDialog()

        self.dialog.tabWidthSpin.SetValue(0)
        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="text":)\n', '\n(:sourceend:)'))

    def testDialogControllerResult5(self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = ["python", "cpp", "haskell", "text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode(wx.ID_OK)
        self.controller.showDialog()

        self.dialog.languageComboBox.SetSelection(0)
        self.dialog.tabWidthSpin.SetValue(0)
        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="cpp":)\n', '\n(:sourceend:)'))

    def testDialogControllerResult6(self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = ["python", "cpp", "haskell", "text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode(wx.ID_OK)
        self.controller.showDialog()

        self.dialog.languageComboBox.SetSelection(1)
        self.dialog.tabWidthSpin.SetValue(0)
        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="haskell":)\n', '\n(:sourceend:)'))

    def testSourceConfig1(self):
        self.config.defaultLanguage.value = "python"
        self.config.tabWidth.value = 8
        self.config.dialogWidth.value = 100
        self.config.dialogHeight.value = 200
        self.config.languageList.value = ["python", "cpp", "haskell"]

        self.assertEqual(self.config.defaultLanguage.value, "python")
        self.assertEqual(self.config.tabWidth.value, 8)
        self.assertEqual(self.config.dialogWidth.value, 100)
        self.assertEqual(self.config.dialogHeight.value, 200)
        self.assertEqual(self.config.languageList.value,
                         ["python", "cpp", "haskell"])

    def testDialogLanguageValues1(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "haskell"

        self.controller.showDialog()

        self.assertEqual(self.dialog.languageComboBox.GetItems(),
                         ["cpp", "haskell", "python"])

        self.assertEqual(self.dialog.languageComboBox.GetSelection(), 1)
        self.assertEqual(self.dialog.languageComboBox.GetValue(), "haskell")

        self.assertEqual(self.dialog.tabWidthSpin.GetValue(), 0)

    def testDialogLanguageValues2(self):
        self.config.languageList.value = []
        self.config.defaultLanguage.value = "haskell"

        self.controller.showDialog()

        self.assertEqual(self.dialog.languageComboBox.GetItems(), ["text"])

        self.assertEqual(self.dialog.languageComboBox.GetSelection(), 0)
        self.assertEqual(self.dialog.languageComboBox.GetValue(), "text")

    def testDialogLanguageValues3(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "c"

        self.controller.showDialog()

        self.assertEqual(self.dialog.languageComboBox.GetItems(), [
                         "cpp", "haskell", "python"])

        self.assertEqual(self.dialog.languageComboBox.GetSelection(), 0)
        self.assertEqual(self.dialog.languageComboBox.GetValue(), "cpp")

    def testDialogLanguageValues4(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "   haskell   "

        self.controller.showDialog()

        self.assertEqual(self.dialog.languageComboBox.GetItems(),
                         ["cpp", "haskell", "python"])

        self.assertEqual(self.dialog.languageComboBox.GetSelection(), 1)
        self.assertEqual(self.dialog.languageComboBox.GetValue(), "haskell")

        self.assertEqual(self.dialog.tabWidthSpin.GetValue(), 0)

    def testDialogStyleValues1(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()

        self.assertEqual(self.dialog.styleComboBox.GetCount(),
                         self._stylesCount)
        self.assertEqual(self.dialog.styleComboBox.GetValue(), "default")

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python":)\n', '\n(:sourceend:)'))

    def testDialogStyleValues2(self):
        self.config.defaultStyle.value = "blablabla"
        self.controller.showDialog()

        self.assertEqual(self.dialog.styleComboBox.GetCount(),
                         self._stylesCount)
        self.assertEqual(self.dialog.styleComboBox.GetValue(), "default")

    def testDialogStyleValues3(self):
        self.config.defaultStyle.value = ""
        self.controller.showDialog()

        self.assertEqual(self.dialog.styleComboBox.GetCount(),
                         self._stylesCount)
        self.assertEqual(self.dialog.styleComboBox.GetValue(), "default")

    def testDialogStyleValues4(self):
        self.config.defaultStyle.value = "vim"
        self.controller.showDialog()

        self.assertEqual(self.dialog.styleComboBox.GetCount(),
                         self._stylesCount)
        self.assertEqual(self.dialog.styleComboBox.GetValue(), "vim")

    def testDialogStyleValues5(self):
        self.config.defaultStyle.value = "emacs"
        self.controller.showDialog()

        self.assertEqual(self.dialog.styleComboBox.GetCount(),
                         self._stylesCount)
        self.assertEqual(self.dialog.styleComboBox.GetValue(), "emacs")

    def testDialogStyle1(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"
        self.config.defaultStyle.value = "vim"
        self.config.style.value = "vim"

        self.controller.showDialog()

        self.assertEqual(self.dialog.styleComboBox.GetCount(),
                         self._stylesCount)
        self.assertEqual(self.dialog.styleComboBox.GetValue(), "vim")

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python":)\n', '\n(:sourceend:)'))

    def testDialogStyle2(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"
        self.config.defaultStyle.value = "vim"
        self.config.style.value = "default"

        self.controller.showDialog()

        self.assertEqual(self.dialog.styleComboBox.GetCount(),
                         self._stylesCount)
        self.assertEqual(self.dialog.styleComboBox.GetValue(), "default")

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python" style="default":)\n', '\n(:sourceend:)'))

    def testDialogStyleText(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()
        self.dialog.styleComboBox.SetSelection(0)

        self.assertEqual(self.dialog.styleComboBox.GetValue(), "abap")
        self.assertEqual(self.dialog.style, "abap")

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python" style="abap":)\n', '\n(:sourceend:)'))

    def testDialogStyleFile(self):
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.dialog.styleComboBox.SetSelection(0)
        self.dialog.attachmentComboBox.SetSelection(0)

        self.assertEqual(self.dialog.styleComboBox.GetValue(), "abap")
        self.assertEqual(self.dialog.style, "abap")

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" lang="python" style="abap":)', '(:sourceend:)'))

    def testDialogStyleFile2(self):
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.dialog.styleComboBox.SetSelection(0)
        self.dialog.attachmentComboBox.SetSelection(0)
        self.dialog.languageComboBox.SetSelection(0)

        self.assertEqual(self.dialog.styleComboBox.GetValue(), "abap")
        self.assertEqual(self.dialog.style, "abap")

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" style="abap":)', '(:sourceend:)'))

    def testDialogStyleText2(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()
        self.dialog.styleComboBox.SetSelection(0)
        self.dialog.tabWidthSpin.SetValue(5)

        self.assertEqual(self.dialog.styleComboBox.GetValue(), "abap")
        self.assertEqual(self.dialog.style, "abap")

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python" tabwidth="5" style="abap":)\n', '\n(:sourceend:)'))

    def testStyleConfig1(self):
        self.config.style.value = "default"

        self.controller.showDialog()
        self.assertEqual(self.dialog.style, "default")

    def testStyleConfig2(self):
        self.config.style.value = "vim"

        self.controller.showDialog()
        self.assertEqual(self.dialog.style, "vim")

    def testStyleConfig3(self):
        self.config.style.value = "  vim   "

        self.controller.showDialog()
        self.assertEqual(self.dialog.style, "vim")

    def testStyleConfig4(self):
        self.config.style.value = "invalid_style"

        self.controller.showDialog()
        self.assertEqual(self.dialog.style, "default")

    def testStyleConfig5(self):
        self.controller.showDialog()
        self.assertEqual(self.dialog.style, "default")

    def testParentBgConfig1(self):
        self.config.parentbg.value = "  False  "
        self.controller.showDialog()

        self.assertEqual(self.dialog.parentbg, False)

    def testParentBgConfig2(self):
        self.config.parentbg.value = "  True  "
        self.controller.showDialog()

        self.assertEqual(self.dialog.parentbg, True)

    def testParentBgConfig3(self):
        self.config.parentbg.value = "  блаблабла  "
        self.controller.showDialog()

        self.assertEqual(self.dialog.parentbg, False)

    def testParentBgConfig4(self):
        # Если нет вообще записей в файле настроек
        self.controller.showDialog()

        self.assertEqual(self.dialog.parentbg, False)

    def testLineNumConfig1(self):
        # Если нет вообще записей в файле настроек
        self.controller.showDialog()

        self.assertEqual(self.dialog.lineNum, False)

    def testLineNumConfig2(self):
        self.config.lineNum.value = "  False  "
        self.controller.showDialog()

        self.assertEqual(self.dialog.lineNum, False)

    def testLineNumConfig3(self):
        self.config.lineNum.value = "  блаблабла  "
        self.controller.showDialog()

        self.assertEqual(self.dialog.lineNum, False)

    def testLineNumConfig4(self):
        self.config.lineNum.value = "True"
        self.controller.showDialog()

        self.assertEqual(self.dialog.lineNum, True)

    def testDialogParengBg(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()
        self.dialog.parentBgCheckBox.SetValue(True)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python" parentbg:)\n', '\n(:sourceend:)'))

    def testDialogLineNum(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()
        self.dialog.lineNumCheckBox.SetValue(True)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python" linenum:)\n', '\n(:sourceend:)'))

    def testDialogParentBgLineNum(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()
        self.dialog.parentBgCheckBox.SetValue(True)
        self.dialog.lineNumCheckBox.SetValue(True)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python" parentbg linenum:)\n', '\n(:sourceend:)'))

    def testDialogTabWidth(self):
        self.config.languageList.value = ["python", "cpp", "haskell"]
        self.config.defaultLanguage.value = "python"

        self.controller.showDialog()
        self.dialog.tabWidthSpin.SetValue(10)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source lang="python" tabwidth="10":)\n', '\n(:sourceend:)'))

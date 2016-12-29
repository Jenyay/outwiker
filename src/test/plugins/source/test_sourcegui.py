# -*- coding: UTF-8 -*-

import unittest
import os.path
from tempfile import mkdtemp

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.utils import removeDir
from .sourcefakedialog import FakeInsertDialog


class SourceGuiPluginTest (unittest.TestCase):
    """
    Тесты интерфейса для плагина Source
    """

    def setUp(self):
        self.__pluginname = u"Source"

        self.__createWiki()

        dirlist = [u"../plugins/source"]
        self._stylesCount = 26

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        self.config = self.loader[self.__pluginname].config
        self._clearConfig(self.config)

        from source.insertdialogcontroller import InsertDialogController
        self.dialog = FakeInsertDialog ()
        self.controller = InsertDialogController(self.testPage, self.dialog, self.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]


    def tearDown(self):
        self._clearConfig (self.config)
        removeDir (self.path)
        self.loader.clear()


    def _clearConfig (self, config):
        Application.config.remove_section (self.config.section)


    def testDialogController1 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.dialog.SetReturnCode (wx.ID_CANCEL)
        result = self.controller.showDialog()

        self.assertEqual (result, wx.ID_CANCEL)


    def testDialogController2 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.dialog.SetReturnCode (wx.ID_OK)
        result = self.controller.showDialog()

        self.assertEqual (result, wx.ID_OK)


    def testDialogControllerResult1 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode (wx.ID_OK)
        self.controller.showDialog()

        self.dialog.tabWidthSpin.SetValue (4)
        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="text" tabwidth="4":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult2 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.defaultLanguage.value = "python"

        self.dialog.SetReturnCode (wx.ID_OK)
        self.controller.showDialog()

        self.dialog.tabWidthSpin.SetValue (8)
        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" tabwidth="8":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult3 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode (wx.ID_OK)
        self.controller.showDialog()

        self.dialog.tabWidthSpin.SetValue (4)
        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="text" tabwidth="4":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult4 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode (wx.ID_OK)
        self.controller.showDialog()

        self.dialog.tabWidthSpin.SetValue (0)
        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="text":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult5 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode (wx.ID_OK)
        self.controller.showDialog()

        self.dialog.languageComboBox.SetSelection (0)
        self.dialog.tabWidthSpin.SetValue (0)
        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="cpp":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult6 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        self.dialog.SetReturnCode (wx.ID_OK)
        self.controller.showDialog()

        self.dialog.languageComboBox.SetSelection (1)
        self.dialog.tabWidthSpin.SetValue (0)
        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="haskell":)\n', u'\n(:sourceend:)'))


    def testSourceConfig1 (self):
        self.config.defaultLanguage.value = u"python"
        self.config.tabWidth.value = 8
        self.config.dialogWidth.value = 100
        self.config.dialogHeight.value = 200
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]

        self.assertEqual (self.config.defaultLanguage.value, u"python")
        self.assertEqual (self.config.tabWidth.value, 8)
        self.assertEqual (self.config.dialogWidth.value, 100)
        self.assertEqual (self.config.dialogHeight.value, 200)
        self.assertEqual (self.config.languageList.value,
                          [u"python", u"cpp", u"haskell"])


    def testDialogLanguageValues1 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"haskell"

        self.controller.showDialog()

        self.assertEqual (self.dialog.languageComboBox.GetItems(),
                          [u"cpp", u"haskell", u"python"])

        self.assertEqual (self.dialog.languageComboBox.GetSelection(), 1)
        self.assertEqual (self.dialog.languageComboBox.GetValue(), u"haskell")

        self.assertEqual (self.dialog.tabWidthSpin.GetValue(), 0)


    def testDialogLanguageValues2 (self):
        self.config.languageList.value = []
        self.config.defaultLanguage.value = u"haskell"

        self.controller.showDialog()

        self.assertEqual (self.dialog.languageComboBox.GetItems(), [u"text"])

        self.assertEqual (self.dialog.languageComboBox.GetSelection(), 0)
        self.assertEqual (self.dialog.languageComboBox.GetValue(), u"text")


    def testDialogLanguageValues3 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"c"

        self.controller.showDialog()

        self.assertEqual (self.dialog.languageComboBox.GetItems(), [u"cpp", u"haskell", u"python"])

        self.assertEqual (self.dialog.languageComboBox.GetSelection(), 0)
        self.assertEqual (self.dialog.languageComboBox.GetValue(), u"cpp")


    def testDialogLanguageValues4 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"   haskell   "

        self.controller.showDialog()

        self.assertEqual (self.dialog.languageComboBox.GetItems(),
                          [u"cpp", u"haskell", u"python"])

        self.assertEqual (self.dialog.languageComboBox.GetSelection(), 1)
        self.assertEqual (self.dialog.languageComboBox.GetValue(), u"haskell")

        self.assertEqual (self.dialog.tabWidthSpin.GetValue(), 0)


    def testDialogStyleValues1 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()

        self.assertEqual (self.dialog.styleComboBox.GetCount(), self._stylesCount)
        self.assertEqual (self.dialog.styleComboBox.GetValue(), "default")

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python":)\n', u'\n(:sourceend:)'))


    def testDialogStyleValues2 (self):
        self.config.defaultStyle.value = "blablabla"
        self.controller.showDialog()

        self.assertEqual (self.dialog.styleComboBox.GetCount(), self._stylesCount)
        self.assertEqual (self.dialog.styleComboBox.GetValue(), "default")


    def testDialogStyleValues3 (self):
        self.config.defaultStyle.value = ""
        self.controller.showDialog()

        self.assertEqual (self.dialog.styleComboBox.GetCount(), self._stylesCount)
        self.assertEqual (self.dialog.styleComboBox.GetValue(), "default")


    def testDialogStyleValues4 (self):
        self.config.defaultStyle.value = "vim"
        self.controller.showDialog()

        self.assertEqual (self.dialog.styleComboBox.GetCount(), self._stylesCount)
        self.assertEqual (self.dialog.styleComboBox.GetValue(), "vim")


    def testDialogStyleValues5 (self):
        self.config.defaultStyle.value = "emacs"
        self.controller.showDialog()

        self.assertEqual (self.dialog.styleComboBox.GetCount(), self._stylesCount)
        self.assertEqual (self.dialog.styleComboBox.GetValue(), "emacs")


    def testDialogStyle1 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"
        self.config.defaultStyle.value = u"vim"
        self.config.style.value = u"vim"

        self.controller.showDialog()

        self.assertEqual (self.dialog.styleComboBox.GetCount(), self._stylesCount)
        self.assertEqual (self.dialog.styleComboBox.GetValue(), "vim")

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python":)\n', u'\n(:sourceend:)'))


    def testDialogStyle2 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"
        self.config.defaultStyle.value = u"vim"
        self.config.style.value = u"default"

        self.controller.showDialog()

        self.assertEqual (self.dialog.styleComboBox.GetCount(), self._stylesCount)
        self.assertEqual (self.dialog.styleComboBox.GetValue(), "default")

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" style="default":)\n', u'\n(:sourceend:)'))


    def testDialogStyleText (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()
        self.dialog.styleComboBox.SetSelection (0)

        self.assertEqual (self.dialog.styleComboBox.GetValue(), "algol")
        self.assertEqual (self.dialog.style, "algol")

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" style="algol":)\n', u'\n(:sourceend:)'))


    def testDialogStyleFile (self):
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.dialog.styleComboBox.SetSelection (0)
        self.dialog.attachmentComboBox.SetSelection (0)

        self.assertEqual (self.dialog.styleComboBox.GetValue(), "algol")
        self.assertEqual (self.dialog.style, "algol")

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" lang="python" style="algol":)', u'(:sourceend:)'))


    def testDialogStyleFile2 (self):
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.dialog.styleComboBox.SetSelection (0)
        self.dialog.attachmentComboBox.SetSelection (0)
        self.dialog.languageComboBox.SetSelection (0)

        self.assertEqual (self.dialog.styleComboBox.GetValue(), "algol")
        self.assertEqual (self.dialog.style, "algol")

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" style="algol":)', u'(:sourceend:)'))


    def testDialogStyleText2 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()
        self.dialog.styleComboBox.SetSelection (0)
        self.dialog.tabWidthSpin.SetValue (5)

        self.assertEqual (self.dialog.styleComboBox.GetValue(), "algol")
        self.assertEqual (self.dialog.style, "algol")

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" tabwidth="5" style="algol":)\n', u'\n(:sourceend:)'))


    def testStyleConfig1 (self):
        self.config.style.value = "default"

        self.controller.showDialog ()
        self.assertEqual (self.dialog.style, "default")


    def testStyleConfig2 (self):
        self.config.style.value = "vim"

        self.controller.showDialog ()
        self.assertEqual (self.dialog.style, "vim")


    def testStyleConfig3 (self):
        self.config.style.value = "  vim   "

        self.controller.showDialog ()
        self.assertEqual (self.dialog.style, "vim")


    def testStyleConfig4 (self):
        self.config.style.value = "invalid_style"

        self.controller.showDialog ()
        self.assertEqual (self.dialog.style, "default")


    def testStyleConfig5 (self):
        self.controller.showDialog ()
        self.assertEqual (self.dialog.style, "default")


    def testParentBgConfig1 (self):
        self.config.parentbg.value = u"  False  "
        self.controller.showDialog ()

        self.assertEqual (self.dialog.parentbg, False)


    def testParentBgConfig2 (self):
        self.config.parentbg.value = u"  True  "
        self.controller.showDialog ()

        self.assertEqual (self.dialog.parentbg, True)


    def testParentBgConfig3 (self):
        self.config.parentbg.value = u"  блаблабла  "
        self.controller.showDialog ()

        self.assertEqual (self.dialog.parentbg, False)


    def testParentBgConfig4 (self):
        # Если нет вообще записей в файле настроек
        self.controller.showDialog ()

        self.assertEqual (self.dialog.parentbg, False)


    def testLineNumConfig1 (self):
        # Если нет вообще записей в файле настроек
        self.controller.showDialog ()

        self.assertEqual (self.dialog.lineNum, False)


    def testLineNumConfig2 (self):
        self.config.lineNum.value = u"  False  "
        self.controller.showDialog ()

        self.assertEqual (self.dialog.lineNum, False)


    def testLineNumConfig3 (self):
        self.config.lineNum.value = u"  блаблабла  "
        self.controller.showDialog ()

        self.assertEqual (self.dialog.lineNum, False)


    def testLineNumConfig4 (self):
        self.config.lineNum.value = u"True"
        self.controller.showDialog ()

        self.assertEqual (self.dialog.lineNum, True)


    def testDialogParengBg (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()
        self.dialog.parentBgCheckBox.SetValue (True)

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" parentbg:)\n', u'\n(:sourceend:)'))


    def testDialogLineNum (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()
        self.dialog.lineNumCheckBox.SetValue (True)

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" linenum:)\n', u'\n(:sourceend:)'))


    def testDialogParentBgLineNum (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()
        self.dialog.parentBgCheckBox.SetValue (True)
        self.dialog.lineNumCheckBox.SetValue (True)

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" parentbg linenum:)\n', u'\n(:sourceend:)'))


    def testDialogTabWidth (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"python"

        self.controller.showDialog()
        self.dialog.tabWidthSpin.SetValue (10)

        result = self.controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" tabwidth="10":)\n', u'\n(:sourceend:)'))

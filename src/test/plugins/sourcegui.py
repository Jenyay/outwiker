#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.utils import removeWiki
from test.fakewx.spinctrl import SpinCtrl
from test.fakewx.combobox import ComboBox
from test.fakewx.dialog import Dialog
from test.fakewx.statictext import StaticText
from test.fakewx.checkbox import CheckBox


class FakeInsertDialog (Dialog):
    """
    Заглушка вместо реального диалога для вставки команды (:source:)
    """
    def __init__ (self):
        super (FakeInsertDialog, self).__init__ ()

        # Заглушки вместо интерфейса
        self.tabWidthSpin = SpinCtrl ()
        self.languageComboBox = ComboBox ()

        self.fileCheckBox = CheckBox()

        self.attachmentLabel = StaticText ()
        self.attachmentComboBox = ComboBox ()

        self.encodingLabel = StaticText ()
        self.encodingComboBox = ComboBox ()


    @property
    def language (self):
        return self.languageComboBox.GetValue()


    @property
    def tabWidth (self):
        return self.tabWidthSpin.GetValue()


    @property
    def languageIndex (self):
        return self.languageComboBox.GetCurrentSelection()


    @property
    def attachment (self):
        return self.attachmentComboBox.GetValue()


    @property
    def encoding (self):
        return self.encodingComboBox.GetValue()


    @property
    def insertFromFile (self):
        return self.fileCheckBox.IsChecked()


class SourceGuiPluginTest (unittest.TestCase):
    """
    Тесты интерфейса для плагина Source
    """
    def setUp(self):
        self.__pluginname = u"Source"

        self.__createWiki()

        dirlist = [u"../plugins/source"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()
        

    def __readFile (self, path):
        with open (path) as fp:
            result = unicode (fp.read(), "utf8")

        return result
    

    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]
        

    def tearDown(self):
        removeWiki (self.path)
        self.loader.clear()


    def testDialogController1 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_CANCEL)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        result = controller.showDialog()

        self.assertEqual (result, wx.ID_CANCEL)


    def testDialogController2 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        result = controller.showDialog()

        self.assertEqual (result, wx.ID_OK)


    def testDialogControllerResult1 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.tabWidthSpin.SetValue (4)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="text" tabwidth="4":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult2 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.defaultLanguage.value = "python"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.tabWidthSpin.SetValue (8)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" tabwidth="8":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult3 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.tabWidthSpin.SetValue (4)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="text" tabwidth="4":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult4 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.tabWidthSpin.SetValue (0)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="text":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult5 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.languageComboBox.SetSelection (0)
        dialog.tabWidthSpin.SetValue (0)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="cpp":)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult6 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.languageComboBox.SetSelection (1)
        dialog.tabWidthSpin.SetValue (0)
        result = controller.getCommandStrings()

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


    def testDialogValues1 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"haskell"

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.languageComboBox.GetItems(), 
                [u"cpp", u"haskell", u"python"])

        self.assertEqual (dialog.languageComboBox.GetSelection(), 1)
        self.assertEqual (dialog.languageComboBox.GetValue(), u"haskell")

        self.assertEqual (dialog.tabWidthSpin.GetValue(), 0)


    def testDialogValues2 (self):
        self.config.languageList.value = []
        self.config.defaultLanguage.value = u"haskell"

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.languageComboBox.GetItems(), [u"text"])

        self.assertEqual (dialog.languageComboBox.GetSelection(), 0)
        self.assertEqual (dialog.languageComboBox.GetValue(), u"text")


    def testDialogValues3 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"c"

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.languageComboBox.GetItems(), [u"cpp", u"haskell", u"python"])

        self.assertEqual (dialog.languageComboBox.GetSelection(), 0)
        self.assertEqual (dialog.languageComboBox.GetValue(), u"cpp")


    def testAttachment1 (self):
        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.attachmentComboBox.GetCount(), 0)


    def testAttachment2 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.attachmentComboBox.GetSelection(), 0)
        self.assertEqual (dialog.attachmentComboBox.GetCount(), 2)
        self.assertEqual (dialog.attachmentComboBox.GetItems(), 
                [u"source_cp1251.cs", u"source_utf8.py"])


    def testAttachment3 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)
        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (0)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs":)', u'(:sourceend:)'))


    def testAttachment4 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)
        dialog.attachmentComboBox.SetSelection (1)
        dialog.encodingComboBox.SetSelection (0)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_utf8.py":)', u'(:sourceend:)'))


    def testAttachment5 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)
        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (2)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" encoding="cp1251":)', u'(:sourceend:)'))


    def testAttachment6 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"cpp", u"csharp", u"haskell"]

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        controller.loadLanguagesState()

        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (2)
        dialog.languageComboBox.SetSelection (3)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" lang="haskell" encoding="cp1251":)', u'(:sourceend:)'))


    def testAttachment7 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"cpp", u"haskell", u"csharp"]

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)
        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (2)
        dialog.languageComboBox.SetSelection (0)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" encoding="cp1251":)', u'(:sourceend:)'))


    def testAttachment8 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"cpp", u"csharp", u"haskell"]

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        controller.loadLanguagesState()

        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (0)
        dialog.languageComboBox.SetSelection (2)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" lang="csharp":)', u'(:sourceend:)'))


    def testAttachment9 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"cpp", u"csharp", u"haskell"]

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        controller.loadLanguagesState()

        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (0)
        dialog.languageComboBox.SetSelection (2)
        dialog.tabWidthSpin.SetValue (10)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" lang="csharp" tabwidth="10":)', u'(:sourceend:)'))

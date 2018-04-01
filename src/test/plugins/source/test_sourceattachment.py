# -*- coding: utf-8 -*-

import os.path
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.basetestcases import BaseOutWikerGUIMixin
from .sourcefakedialog import FakeInsertDialog


class SourceAttachmentPluginTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты интерфейса для плагина Source
    """

    def setUp(self):
        self.__pluginname = "Source"
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        dirlist = ["../plugins/source"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()
        self.application.config.remove_section(self.config.section)

        from source.insertdialogcontroller import InsertDialogController
        self.dialog = FakeInsertDialog()
        self.controller = InsertDialogController(
            self.testPage, self.dialog, self.config)

    def tearDown(self):
        self.application.config.remove_section(self.config.section)
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testAttachment1(self):
        self.controller.showDialog()

        self.assertEqual(self.dialog.attachmentComboBox.GetCount(), 0)

    def testAttachment2(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.controller.showDialog()

        self.assertEqual(self.dialog.attachmentComboBox.GetSelection(), 0)
        self.assertEqual(self.dialog.attachmentComboBox.GetCount(), 2)
        self.assertEqual(self.dialog.attachmentComboBox.GetItems(),
                         ["source_cp1251.cs", "source_utf8.py"])

    def testAttachment3(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.controller.updateFileChecked()

        self.dialog.attachmentComboBox.SetSelection(0)
        self.dialog.encodingComboBox.SetSelection(0)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs":)', '(:sourceend:)'))

    def testAttachment4(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.controller.updateFileChecked()

        self.dialog.attachmentComboBox.SetSelection(1)
        self.dialog.encodingComboBox.SetSelection(0)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_utf8.py":)', '(:sourceend:)'))

    def testAttachment5(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.controller.updateFileChecked()

        self.dialog.attachmentComboBox.SetSelection(0)
        self.dialog.encodingComboBox.SetSelection(2)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" encoding="cp1251":)', '(:sourceend:)'))

    def testAttachment6(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["cpp", "csharp", "haskell"]

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        self.controller.loadLanguagesState()

        self.dialog.attachmentComboBox.SetSelection(0)
        self.dialog.encodingComboBox.SetSelection(2)
        self.dialog.languageComboBox.SetSelection(3)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" encoding="cp1251" lang="haskell":)', '(:sourceend:)'))

    def testAttachment7(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["cpp", "haskell", "csharp"]

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.dialog.attachmentComboBox.SetSelection(0)
        self.dialog.encodingComboBox.SetSelection(2)
        self.dialog.languageComboBox.SetSelection(0)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" encoding="cp1251":)', '(:sourceend:)'))

    def testAttachment8(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["cpp", "csharp", "haskell"]

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        self.controller.loadLanguagesState()

        self.dialog.attachmentComboBox.SetSelection(0)
        self.dialog.encodingComboBox.SetSelection(0)
        self.dialog.languageComboBox.SetSelection(2)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" lang="csharp":)', '(:sourceend:)'))

    def testAttachment9(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["cpp", "csharp", "haskell"]

        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        self.controller.loadLanguagesState()

        self.dialog.attachmentComboBox.SetSelection(0)
        self.dialog.encodingComboBox.SetSelection(0)
        self.dialog.languageComboBox.SetSelection(2)
        self.dialog.tabWidthSpin.SetValue(10)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" lang="csharp" tabwidth="10":)', '(:sourceend:)'))

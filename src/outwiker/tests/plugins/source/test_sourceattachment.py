# -*- coding: utf-8 -*-

import os.path
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.attachment import Attachment
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class SourceAttachmentPluginTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты интерфейса для плагина Source
    """

    def setUp(self):
        self.__pluginname = "Source"
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        dirlist = ["plugins/source"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()
        self.application.config.remove_section(self.config.section)

        from source.insertdialogcontroller import InsertDialogController
        from source.insertdialog import InsertDialog
        self.dialog = InsertDialog(self.application.mainWindow)
        self.controller = InsertDialogController(
            self.testPage, self.dialog, self.config)

    def tearDown(self):
        self.application.config.remove_section(self.config.section)
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testAttachment1(self):
        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.assertEqual(self.dialog.attachmentComboBox.GetCount(), 0)

    def testAttachment2(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.assertEqual(self.dialog.attachmentComboBox.GetCount(), 3)
        self.assertEqual(self.dialog.attachmentComboBox.GetFilesListRelative(),
                         ["source_cp1251.cs", "source_utf8.py"])

    def testAttachment3(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.controller.updateFileChecked()

        self.dialog.attachmentComboBox.SetValue("source_cp1251.cs")
        self.dialog.encodingComboBox.SetSelection(0)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs":)', '(:sourceend:)'))

    def testAttachment4(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.controller.updateFileChecked()

        self.dialog.attachmentComboBox.SetValue("source_utf8.py")
        self.dialog.encodingComboBox.SetSelection(0)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_utf8.py":)', '(:sourceend:)'))

    def testAttachment5(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.controller.updateFileChecked()

        self.dialog.attachmentComboBox.SetValue("source_cp1251.cs")
        self.dialog.encodingComboBox.SetSelection(2)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" encoding="cp1251":)', '(:sourceend:)'))

    def testAttachment6(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["cpp", "csharp", "haskell"]

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        self.controller.loadLanguagesState()

        self.dialog.attachmentComboBox.SetValue("source_cp1251.cs")
        self.dialog.encodingComboBox.SetSelection(2)
        self.dialog.languageComboBox.SetSelection(3)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" encoding="cp1251" lang="haskell":)', '(:sourceend:)'))

    def testAttachment7(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["cpp", "haskell", "csharp"]

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.dialog.attachmentComboBox.SetValue("source_cp1251.cs")
        self.dialog.encodingComboBox.SetSelection(2)
        self.dialog.languageComboBox.SetSelection(0)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" encoding="cp1251":)', '(:sourceend:)'))

    def testAttachment8(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["cpp", "csharp", "haskell"]

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        self.controller.loadLanguagesState()

        self.dialog.attachmentComboBox.SetValue("source_cp1251.cs")
        self.dialog.encodingComboBox.SetSelection(0)
        self.dialog.languageComboBox.SetSelection(1)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" lang="csharp":)', '(:sourceend:)'))

    def testAttachment9(self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_utf8.py")])
        Attachment(self.testPage).attach(
            [os.path.join(self.samplefilesPath, "source_cp1251.cs")])

        self.config.languageList.value = ["cpp", "csharp", "haskell"]

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        self.controller.loadLanguagesState()

        self.dialog.attachmentComboBox.SetValue("source_cp1251.cs")
        self.dialog.encodingComboBox.SetSelection(0)
        self.dialog.languageComboBox.SetSelection(1)
        self.dialog.tabWidthSpin.SetValue(10)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:source_cp1251.cs" lang="csharp" tabwidth="10":)', '(:sourceend:)'))

    def testAttachment_subdir(self):
        subdir = 'subdir 1/subdir 2/'

        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "testdata/samplefiles/sources"
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)

        files_src = [os.path.join(self.samplefilesPath, fname)
                     for fname
                     in ["source_utf8.py", "source_cp1251.cs"]]

        attach.attach(files_src, subdir=subdir)

        Tester.dialogTester.appendOk()
        self.controller.showDialog()

        self.dialog.fileCheckBox.SetValue(True)
        self.controller.updateFileChecked()

        self.dialog.attachmentComboBox.SetValue(subdir + "source_cp1251.cs")
        self.dialog.encodingComboBox.SetSelection(0)

        result = self.controller.getCommandStrings()

        self.assertEqual(
            result, ('(:source file="Attach:subdir 1/subdir 2/source_cp1251.cs":)', '(:sourceend:)'))

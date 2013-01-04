#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeWiki
from test.fakewx.spinctrl import SpinCtrl
from test.fakewx.combobox import ComboBox
from test.fakewx.dialog import Dialog


class FakeInsertDialog (Dialog):
    """
    Заглушка вместо реального диалога для вставки команды (:source:)
    """
    def __init__ (self):
        super (FakeInsertDialog, self).__init__ ()

        # Заглушки вместо интерфейса
        self.tabWidthSpin = SpinCtrl ()
        self.languageComboBox = ComboBox ()


    @property
    def tabWidth (self):
        """
        Размер табуляции
        """
        return self.tabWidthSpin.GetValue()


    @property
    def language (self):
        """
        Выбранный язык
        """
        return self.languageComboBox.GetValue()



class SourcePluginTest (unittest.TestCase):
    def setUp(self):
        self.__pluginname = u"Source"

        self.__createWiki()

        dirlist = [u"../plugins/source"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()
        
        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


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


    def testPluginLoad (self):
        self.assertEqual ( len (self.loader), 1)
        self.assertGreater (len (self.loader[self.__pluginname].url), 0)


    def testEmptyCommand (self):
        text = u'''bla-bla-bla (:source:) bla-bla-bla'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"bla-bla-bla" in result)


    def testFullHtmlPython (self):
        text = u'''(:source lang="python" tabwidth=5:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'          <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString3 = u'<span class="kn">import</span> <span class="nn">os</span>'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)


    def testFullHtmlPython2 (self):
        text = u'''(:source lang="python":)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'       <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString3 = u'<span class="kn">import</span> <span class="nn">os</span>'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)


    def testFullHtmlPython3 (self):
        # Неправильный размер табуляции
        text = u'''(:source lang="python" tabwidth="qqqqq":)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'       <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString3 = u'<span class="kn">import</span> <span class="nn">os</span>'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)


    def testFullHtmlInvalidLang (self):
        text = u'''(:source lang="qqq" tabwidth=4:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'        print &quot;Hello world!!!&quot;'
        innerString3 = u'def hello (count):'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testFullHtmlText (self):
        text = u'''(:source lang="text" tabwidth=4:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'        print &quot;Hello world!!!&quot;'
        innerString3 = u'def hello (count):'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testFullHtmlText2 (self):
        text = u'''(:source:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'        print &quot;Hello world!!!&quot;'
        innerString3 = u'def hello (count):'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testManySource (self):
        text = u'''(:source lang=python:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)


(:source:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'        print &quot;Hello world!!!&quot;'
        innerString3 = u'def hello (count):'
        innerString4 = u'       <span class="k">print</span> <span class="s">&quot;Hello world!!!&quot;</span>'
        innerString5 = u'<span class="kn">import</span> <span class="nn">os</span>'
        
        self.assertTrue (innerString1 in result)
    
        # Проверка того, что стиль добавился только один раз
        self.assertTrue (result.find (innerString1) == result.rfind (innerString1))

        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertTrue (innerString4 in result)
        self.assertTrue (innerString5 in result)
        self.assertFalse (u"(:source" in result)


    def testConfigTabWidth(self):
        text = u'''(:source:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''
        self.config.tabWidth.value = 10

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'          for i in range (10)'
        innerString3 = u'def hello (count):'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testConfigTabWidth2(self):
        text = u'''(:source tabwidth=10:)
import os

# Комментарий
def hello (count):
	"""
	Hello world
	"""
	for i in range (10):
		print "Hello world!!!"
(:sourceend:)
'''
        self.config.tabWidth.value = 4

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        innerString1 = u".go { color: #808080 } /* Generic.Output */"
        innerString2 = u'          for i in range (10)'
        innerString3 = u'def hello (count):'
        
        self.assertTrue (innerString1 in result)
        self.assertTrue (innerString2 in result)
        self.assertTrue (innerString3 in result)
        self.assertFalse (u"(:source" in result)


    def testDialogController1 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_CANCEL)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
        result = controller.showDialog()

        self.assertEqual (result, wx.ID_CANCEL)


    def testDialogController2 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
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
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
        controller.showDialog()

        dialog.tabWidthSpin.SetValue (4)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="text" tabwidth=4:)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult2 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.defaultLanguage.value = "python"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
        controller.showDialog()

        dialog.tabWidthSpin.SetValue (8)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python" tabwidth=8:)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult3 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
        controller.showDialog()

        dialog.tabWidthSpin.SetValue (4)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="text" tabwidth=4:)\n', u'\n(:sourceend:)'))


    def testDialogControllerResult4 (self):
        """
        Тест контроллера диалога для вставки команды (:source:)
        """
        self.config.languageList.value = [u"python", u"cpp", u"haskell", u"text"]
        self.config.defaultLanguage.value = "text"

        dialog = FakeInsertDialog ()
        dialog.SetReturnCode (wx.ID_OK)
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
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
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
        controller.showDialog()

        dialog.languageComboBox.SetSelection (0)
        dialog.tabWidthSpin.SetValue (0)
        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source lang="python":)\n', u'\n(:sourceend:)'))


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
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.languageComboBox.GetItems(), 
                [u"python", u"cpp", u"haskell"])

        self.assertEqual (dialog.languageComboBox.GetSelection(), 2)
        self.assertEqual (dialog.languageComboBox.GetValue(), u"haskell")

        self.assertEqual (dialog.tabWidthSpin.GetValue(), 0)


    def testDialogValues2 (self):
        self.config.languageList.value = []
        self.config.defaultLanguage.value = u"haskell"

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.languageComboBox.GetItems(), [u"text"])

        self.assertEqual (dialog.languageComboBox.GetSelection(), 0)
        self.assertEqual (dialog.languageComboBox.GetValue(), u"text")


    def testDialogValues3 (self):
        self.config.languageList.value = [u"python", u"cpp", u"haskell"]
        self.config.defaultLanguage.value = u"c"

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.languageComboBox.GetItems(), [u"python", u"cpp", u"haskell"])

        self.assertEqual (dialog.languageComboBox.GetSelection(), 0)
        self.assertEqual (dialog.languageComboBox.GetValue(), u"python")


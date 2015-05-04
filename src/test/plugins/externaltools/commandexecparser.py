# -*- coding: UTF-8 -*-

import unittest
import os.path
from tempfile import mkdtemp

from outwiker.core.attachment import Attachment
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory

from test.utils import removeDir


class CommandExecParserTest (unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.__createWiki()
        self.testPage = self.wikiroot[u'Страница 1']
        self.testPageTextPath = os.path.join (self.testPage.path, u'__page.text')
        self.testPageHtmlPath = os.path.join (self.testPage.path, PAGE_RESULT_HTML)
        self.testPageAttachPath = Attachment(self.testPage).getAttachPath(False)

        dirlist = [u'../plugins/externaltools']

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')
        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u'Страница 1', [])


    def tearDown(self):
        removeDir (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testEmpty (self):
        text = u'(:exec:)(:execend:)'
        validResult = u''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testCommandExecParser_01_empty (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 0)


    def testCommandExecParser_02 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u'gvim'

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (len (result[0].params), 0)


    def testCommandExecParser_03 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u'''gvim
krusader'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 2)

        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (len (result[0].params), 0)

        self.assertEqual (result[1].command, u'krusader')
        self.assertEqual (len (result[1].params), 0)


    def testCommandExecParser_04 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u'''

    gvim  


      krusader   

'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 2)

        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (len (result[0].params), 0)

        self.assertEqual (result[1].command, u'krusader')
        self.assertEqual (len (result[1].params), 0)


    def testCommandExecParser_05_params (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u'gvim -d файл1.txt файл2.txt'

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'-d', u'файл1.txt', u'файл2.txt'])


    def testCommandExecParser_06_params (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u'  gvim   -d   файл1.txt   файл2.txt   '

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'-d', u'файл1.txt', u'файл2.txt'])


    def testCommandExecParser_07_params (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u'  gvim   -d   "Имя файла 1.txt"   "Имя файла 2.txt"   '

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'-d', u'Имя файла 1.txt', u'Имя файла 2.txt'])


    def testCommandExecParser_08_params (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = ur'  gvim   -d   "Имя файла 1\".txt"   "Имя файла 2.txt"   '

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'-d', u'Имя файла 1".txt', u'Имя файла 2.txt'])


    def testCommandExecParser_09_params (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u'''
        gvim   -d   "Имя файла 1.txt"   "Имя файла 2.txt"


        krusader Параметр1 "Параметр 2 с пробелом"

        '''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 2)

        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'-d', u'Имя файла 1.txt', u'Имя файла 2.txt'])

        self.assertEqual (result[1].command, u'krusader')
        self.assertEqual (result[1].params, [u'Параметр1', u'Параметр 2 с пробелом'])


    def testCommandExecParser_10_join (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = ur'''gvim \
"Имя файла"
'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)

        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'Имя файла'])


    def testCommandExecParser_11_join (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = ur'''gvim \   
   "Имя файла"
'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)

        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'Имя файла'])


    def testCommandExecParser_12_join (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = ur'''gvim \


"Имя файла"
'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)

        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'Имя файла'])


    def testCommandExecParser_13_invalid (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = ur'''gvim \ asdfadsf'''

        parser = CommandExecParser (self.testPage)
        parser.parse (text)


    def testCommandExecParser_14_params (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = u'gvim -d'

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'-d'])


    def testMacrosPage_01 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim %page%'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [self.testPageTextPath])


    def testMacrosPage_02 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim %PAGE%'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [self.testPageTextPath])


    def testMacrosHtml_01 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim %html%'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [self.testPageHtmlPath])


    def testMacrosFolder_01 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim %folder%'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [self.testPage.path])


    def testMacrosFolder_02 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim %folder%/111.txt'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [self.testPage.path + u'/111.txt'])


    def testMacrosFolder_03 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim %FOLDER%'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [self.testPage.path])


    def testMacrosAttach_01 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim %attach%'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [self.testPageAttachPath])


    def testMacrosAttach_02 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim %ATTACH%'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [self.testPageAttachPath])


    def testMacrosAttach_03 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim Attach:абырвалг.txt'''

        attachPath = os.path.join (self.testPageAttachPath, u'абырвалг.txt')

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [attachPath])


    def testMacrosAttach_04 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim "Attach:абырвалг главрыба.txt"'''

        attachPath = os.path.join (self.testPageAttachPath, u'абырвалг главрыба.txt')

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [attachPath])


    def testMacrosAttach_05 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim xAttach:абырвалг.txt'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'xAttach:абырвалг.txt'])


    def testMacrosAttach_06 (self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = u'''gvim attach:абырвалг.txt'''

        parser = CommandExecParser (self.testPage)
        result = parser.parse (text)

        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].command, u'gvim')
        self.assertEqual (result[0].params, [u'attach:абырвалг.txt'])

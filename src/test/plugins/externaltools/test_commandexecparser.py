# -*- coding: utf-8 -*-

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
        self.testPage = self.wikiroot['Страница 1']
        self.testPageTextPath = os.path.join(self.testPage.path, '__page.text')
        self.testPageHtmlPath = os.path.join(
            self.testPage.path, PAGE_RESULT_HTML)
        self.testPageAttachPath = Attachment(
            self.testPage).getAttachPath(False)

        dirlist = ['../plugins/externaltools']

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')
        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, 'Страница 1', [])

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testEmpty(self):
        text = '(:exec:)(:execend:)'
        validResult = ''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testCommandExecParser_01_empty(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = ''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 0)

    def testCommandExecParser_02(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = 'gvim'

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(len(result[0].params), 0)

    def testCommandExecParser_03(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = '''gvim
krusader'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(len(result[0].params), 0)

        self.assertEqual(result[1].command, 'krusader')
        self.assertEqual(len(result[1].params), 0)

    def testCommandExecParser_04(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = '''

    gvim


      krusader

'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(len(result[0].params), 0)

        self.assertEqual(result[1].command, 'krusader')
        self.assertEqual(len(result[1].params), 0)

    def testCommandExecParser_05_params(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = 'gvim -d файл1.txt файл2.txt'

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['-d', 'файл1.txt', 'файл2.txt'])

    def testCommandExecParser_06_params(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = '  gvim   -d   файл1.txt   файл2.txt   '

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['-d', 'файл1.txt', 'файл2.txt'])

    def testCommandExecParser_07_params(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = '  gvim   -d   "Имя файла 1.txt"   "Имя файла 2.txt"   '

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(
            result[0].params, [
                '-d', 'Имя файла 1.txt', 'Имя файла 2.txt'])

    def testCommandExecParser_08_params(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = r'  gvim   -d   "Имя файла 1\".txt"   "Имя файла 2.txt"   '

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(
            result[0].params, [
                '-d', 'Имя файла 1".txt', 'Имя файла 2.txt'])

    def testCommandExecParser_09_params(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = '''
        gvim   -d   "Имя файла 1.txt"   "Имя файла 2.txt"


        krusader Параметр1 "Параметр 2 с пробелом"

        '''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(
            result[0].params, [
                '-d', 'Имя файла 1.txt', 'Имя файла 2.txt'])

        self.assertEqual(result[1].command, 'krusader')
        self.assertEqual(
            result[1].params, [
                'Параметр1', 'Параметр 2 с пробелом'])

    def testCommandExecParser_10_join(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = r'''gvim \
"Имя файла"
'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['Имя файла'])

    def testCommandExecParser_11_join(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = r'''gvim \
   "Имя файла"
'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['Имя файла'])

    def testCommandExecParser_join_01(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = r'''gvim \


"Имя файла"
'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['Имя файла'])

    def testCommandExecParser_13_invalid(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = r'''gvim \ asdfadsf'''

        parser = CommandExecParser(self.testPage)
        parser.parse(text)

    def testCommandExecParser_14_params(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = 'gvim -d'

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['-d'])

    def testCommandExecParser_15_params(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser
        text = 'gvim "c:\\temp\\abyrvalg\\rrr\\nnn"'

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['c:\\temp\\abyrvalg\\rrr\\nnn'])

    def testMacrosPage_01(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim %page%'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [self.testPageTextPath])

    def testMacrosPage_02(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim %PAGE%'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['%PAGE%'])

    def testMacrosPage_03(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim \\
%page%'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [self.testPageTextPath])

    def testMacrosHtml_01(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim %html%'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [self.testPageHtmlPath])

    def testMacrosFolder_01(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim %folder%'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [self.testPage.path])

    def testMacrosFolder_02(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim %folder%/111.txt'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [self.testPage.path + '/111.txt'])

    def testMacrosFolder_03(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim %FOLDER%'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['%FOLDER%'])

    def testMacrosAttach_01(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim %attach%'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [self.testPageAttachPath])

    def testMacrosAttach_02(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim %ATTACH%'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['%ATTACH%'])

    def testMacrosAttach_03(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim Attach:абырвалг.txt'''

        attachPath = os.path.join(self.testPageAttachPath, 'абырвалг.txt')

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [attachPath])

    def testMacrosAttach_04(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim "Attach:абырвалг главрыба.txt"'''

        attachPath = os.path.join(
            self.testPageAttachPath,
            'абырвалг главрыба.txt')

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [attachPath])

    def testMacrosAttach_05(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim xAttach:абырвалг.txt'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['xAttach:абырвалг.txt'])

    def testMacrosAttach_06(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim attach:абырвалг.txt'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['attach:абырвалг.txt'])

    def testMacrosApp_01(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''%folder%/gvim'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command,
                         self.testPage.path + '/gvim')

    def testMacrosApp_02(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''%attach%/gvim'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command,
                         self.testPageAttachPath + '/gvim')

    def testComments_01(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim fname
# Комментарий'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['fname'])

    def testComments_02(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim fname

# Комментарий


'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['fname'])

    def testComments_03(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''# Комментарий

gvim fname'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['fname'])

    def testComments_04(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim fname # Комментарий'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['fname', '#', 'Комментарий'])

    def testComments_05(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim fname
#Комментарий'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['fname'])

    def testComments_06(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim fname \\
#Комментарий'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['fname'])

    def testComments_07(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim \\
#Комментарий
fname'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['fname'])

    def testComments_08(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim \\
 #Комментарий'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['#Комментарий'])

    def testComments_09(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim \\
 #Комментарий

'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, ['#Комментарий'])

    def testComments_10(self):
        from externaltools.commandexec.commandexecparser import CommandExecParser

        text = '''gvim
# Комментарий
krusader
# Комментарий 2
'''

        parser = CommandExecParser(self.testPage)
        result = parser.parse(text)

        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].command, 'gvim')
        self.assertEqual(result[0].params, [])

        self.assertEqual(result[1].command, 'krusader')
        self.assertEqual(result[1].params, [])

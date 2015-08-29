# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.commands.dates import CommandDateCreation, CommandDateEdition
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.gui.guiconfig import GeneralGuiConfig


class WikiCommandDatesTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        self._config = GeneralGuiConfig (Application.config)
        self._srcDateFormat = self._config.dateTimeFormat.value

        self.testPage = self.wikiroot[u"Страница 1"]
        self.testPage.creationdatetime = datetime (2014, 8, 20, 11, 59, 1)
        self.testPage.datetime = datetime (2015, 9, 21, 12, 10, 20)

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        factory = WikiPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])


    def tearDown(self):
        removeDir (self.path)
        self._config.dateTimeFormat.value = self._srcDateFormat


    def testCreationEmpty_01 (self):
        self._config.dateTimeFormat.value = u'%d.%m.%Y'

        command = CommandDateCreation (self.parser)
        params = u''

        result = command.execute (params, u'')

        result_right = u"20.08.2014"

        self.assertEqual (result_right, result)


    def testCreationEmpty_02 (self):
        self._config.dateTimeFormat.value = u'%d.%m'

        command = CommandDateCreation (self.parser)
        params = u''

        result = command.execute (params, u'')

        result_right = u"20.08"

        self.assertEqual (result_right, result)


    def testCreationParams_01 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateCreation (self.parser)
        params = u'format="%d.%m.%Y"'

        result = command.execute (params, u'')

        result_right = u"20.08.2014"

        self.assertEqual (result_right, result)


    def testCreationParams_02 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateCreation (self.parser)
        params = u'format = ""'

        result = command.execute (params, u'')

        result_right = u""

        self.assertEqual (result_right, result)


    def testCreationParams_03 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateCreation (self.parser)
        params = u'format="%d.%m Абырвалг"'

        result = command.execute (params, u'')

        result_right = u"20.08 Абырвалг"

        self.assertEqual (result_right, result)


    def testEditEmpty_01 (self):
        self._config.dateTimeFormat.value = u'%d.%m.%Y'

        command = CommandDateEdition (self.parser)
        params = u''

        result = command.execute (params, u'')

        result_right = u"21.09.2015"

        self.assertEqual (result_right, result)


    def testEditEmpty_02 (self):
        self._config.dateTimeFormat.value = u'%d.%m'

        command = CommandDateEdition (self.parser)
        params = u''

        result = command.execute (params, u'')

        result_right = u"21.09"

        self.assertEqual (result_right, result)


    def testEditParams_01 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateEdition (self.parser)
        params = u'format="%d.%m.%Y"'

        result = command.execute (params, u'')

        result_right = u"21.09.2015"

        self.assertEqual (result_right, result)


    def testEditParams_02 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateEdition (self.parser)
        params = u'format = ""'

        result = command.execute (params, u'')

        result_right = u""

        self.assertEqual (result_right, result)


    def testEditParams_03 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateEdition (self.parser)
        params = u'format="%d.%m Абырвалг"'

        result = command.execute (params, u'')

        result_right = u"21.09 Абырвалг"

        self.assertEqual (result_right, result)

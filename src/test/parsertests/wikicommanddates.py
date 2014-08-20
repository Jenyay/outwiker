# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime

from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeWiki
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.commanddates import CommandDateCreation
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.gui.guiconfig import GeneralGuiConfig


class WikiCommandDatesTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        self._config = GeneralGuiConfig (Application.config)
        self._srcDateFormat = self._config.dateTimeFormat.value

        self.testPage = self.rootwiki[u"Страница 1"]
        self.testPage.creationdatetime = datetime (2014, 8, 20, 11, 59, 1)

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        factory = WikiPageFactory()
        factory.create (self.rootwiki, u"Страница 1", [])


    def tearDown(self):
        removeWiki (self.path)
        self._config.dateTimeFormat.value = self._srcDateFormat


    def testEmpty_01 (self):
        self._config.dateTimeFormat.value = u'%d.%m.%Y'

        command = CommandDateCreation (self.parser)
        params = u''

        result = command.execute (params, u'')

        result_right = u"20.08.2014"

        self.assertEqual (result_right, result)


    def testEmpty_02 (self):
        self._config.dateTimeFormat.value = u'%d.%m'

        command = CommandDateCreation (self.parser)
        params = u''

        result = command.execute (params, u'')

        result_right = u"20.08"

        self.assertEqual (result_right, result)


    def testParams_01 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateCreation (self.parser)
        params = u'format="%d.%m.%Y"'

        result = command.execute (params, u'')

        result_right = u"20.08.2014"

        self.assertEqual (result_right, result)


    def testParams_02 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateCreation (self.parser)
        params = u'format = ""'

        result = command.execute (params, u'')

        result_right = u""

        self.assertEqual (result_right, result)


    def testParams_03 (self):
        self._config.dateTimeFormat.value = u'%c'

        command = CommandDateCreation (self.parser)
        params = u'format="%d.%m Абырвалг"'

        result = command.execute (params, u'')

        result_right = u"20.08 Абырвалг"

        self.assertEqual (result_right, result)

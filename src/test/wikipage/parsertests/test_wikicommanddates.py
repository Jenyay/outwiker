# -*- coding: utf-8 -*-

from datetime import datetime
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir
from outwiker.pages.wiki.parser.commands.dates import CommandDateCreation, CommandDateEdition
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.gui.guiconfig import GeneralGuiConfig
from test.basetestcases import BaseOutWikerTest


class WikiCommandDatesTest (BaseOutWikerTest):
    def setUp(self):
        self.initApplication()
        self.encoding = "utf8"

        self.filesPath = "../test/samplefiles/"
        self.__createWiki()

        self._config = GeneralGuiConfig(self.application.config)
        self._srcDateFormat = self._config.dateTimeFormat.value

        self.testPage = self.wikiroot["Страница 1"]
        self.testPage.creationdatetime = datetime(2014, 8, 20, 11, 59, 1)
        self.testPage.datetime = datetime(2015, 9, 21, 12, 10, 20)

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self.application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = WikiPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)
        self._config.dateTimeFormat.value = self._srcDateFormat

    def testCreationEmpty_01(self):
        self._config.dateTimeFormat.value = '%d.%m.%Y'

        command = CommandDateCreation(self.parser)
        params = ''

        result = command.execute(params, '')

        result_right = "20.08.2014"

        self.assertEqual(result_right, result)

    def testCreationEmpty_02(self):
        self._config.dateTimeFormat.value = '%d.%m'

        command = CommandDateCreation(self.parser)
        params = ''

        result = command.execute(params, '')

        result_right = "20.08"

        self.assertEqual(result_right, result)

    def testCreationParams_01(self):
        self._config.dateTimeFormat.value = '%c'

        command = CommandDateCreation(self.parser)
        params = 'format="%d.%m.%Y"'

        result = command.execute(params, '')

        result_right = "20.08.2014"

        self.assertEqual(result_right, result)

    def testCreationParams_02(self):
        self._config.dateTimeFormat.value = '%c'

        command = CommandDateCreation(self.parser)
        params = 'format = ""'

        result = command.execute(params, '')

        result_right = ""

        self.assertEqual(result_right, result)

    def testCreationParams_03(self):
        self._config.dateTimeFormat.value = '%c'

        command = CommandDateCreation(self.parser)
        params = 'format="%d.%m Абырвалг"'

        result = command.execute(params, '')

        result_right = "20.08 Абырвалг"

        self.assertEqual(result_right, result)

    def testEditEmpty_01(self):
        self._config.dateTimeFormat.value = '%d.%m.%Y'

        command = CommandDateEdition(self.parser)
        params = ''

        result = command.execute(params, '')

        result_right = "21.09.2015"

        self.assertEqual(result_right, result)

    def testEditEmpty_02(self):
        self._config.dateTimeFormat.value = '%d.%m'

        command = CommandDateEdition(self.parser)
        params = ''

        result = command.execute(params, '')

        result_right = "21.09"

        self.assertEqual(result_right, result)

    def testEditParams_01(self):
        self._config.dateTimeFormat.value = '%c'

        command = CommandDateEdition(self.parser)
        params = 'format="%d.%m.%Y"'

        result = command.execute(params, '')

        result_right = "21.09.2015"

        self.assertEqual(result_right, result)

    def testEditParams_02(self):
        self._config.dateTimeFormat.value = '%c'

        command = CommandDateEdition(self.parser)
        params = 'format = ""'

        result = command.execute(params, '')

        result_right = ""

        self.assertEqual(result_right, result)

    def testEditParams_03(self):
        self._config.dateTimeFormat.value = '%c'

        command = CommandDateEdition(self.parser)
        params = 'format="%d.%m Абырвалг"'

        result = command.execute(params, '')

        result_right = "21.09 Абырвалг"

        self.assertEqual(result_right, result)

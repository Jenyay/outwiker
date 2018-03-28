# -*- coding: utf-8 -*-

import os
import os.path
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.style import Style
from outwiker.core.defines import PAGE_RESULT_HTML

from outwiker.gui.guiconfig import HtmlRenderConfig

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlcache import HtmlCache
from outwiker.pages.wiki.emptycontent import EmptyContent
from outwiker.pages.wiki.wikiconfig import WikiConfig

from test.utils import removeDir
from test.basetestcases import BaseOutWikerTest


class WikiHtmlCacheTest (BaseOutWikerTest):
    def setUp(self):
        self.initApplication()
        self.filesPath = "../test/samplefiles/"
        self.__createWiki()

        files = ["image.jpg", "dir"]

        fullFilesPath = [
            os.path.join(
                self.filesPath,
                fname) for fname in files]

        self.attach_page2 = Attachment(self.wikiroot["Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

        self.wikitext = """Бла-бла-бла
        %thumb maxsize=250%Attach:image.jpg%%
        Бла-бла-бла"""

        self.testPage.content = self.wikitext

        self.__htmlconfig = HtmlRenderConfig(self.application.config)
        self.__setDefaultConfig()

        self.resultPath = os.path.join(self.testPage.path, PAGE_RESULT_HTML)

    def __setDefaultConfig(self):
        # Установим размер превьюшки, не совпадающий с размером по умолчанию
        self.application.config.set(WikiConfig.WIKI_SECTION,
                                    WikiConfig.THUMB_SIZE_PARAM,
                                    WikiConfig.THUMB_SIZE_DEFAULT)

        self.application.config.set(HtmlRenderConfig.HTML_SECTION,
                                    HtmlRenderConfig.FONT_FACE_NAME_PARAM,
                                    HtmlRenderConfig.FONT_NAME_DEFAULT)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def testCache1(self):
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        # После того, как один раз сгенерили страницу, если ничего не
        # изменилось, можно кешировать
        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        self.testPage.content = "бла-бла-бла"

        # Изменили содержимое страницы, опять нельзя кешировать
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

        # Добавим файл
        attach = Attachment(self.testPage)
        attach.attach([os.path.join(self.filesPath, "add.png")])

        self.assertFalse(cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

    def testCacheRename(self):
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # После того, как один раз сгенерили страницу, если ничего не
        # изменилось, можно кешировать
        self.assertTrue(cache.canReadFromCache())

        self.testPage.content = "бла-бла-бла"

        # Изменили содержимое страницы, опять нельзя кешировать
        self.assertFalse(cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

        # Изменили заголовок
        self.testPage.title = "Новый заголовок"

        self.assertFalse(cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

    def testCacheEmpty(self):
        emptycontent = EmptyContent(self.application.config)
        self.testPage.content = ""

        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)

        self.assertFalse(cache.canReadFromCache())
        cache.saveHash()

        # Страница пустая, изменился шаблон для путой записи
        emptycontent.content = "1111"
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # Изменилось содержимое страницы
        self.testPage.content = "Бла-бла-бла"
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())
        cache.saveHash()

        # Изменился шаблон страницы, но страница уже не пустая
        emptycontent.content = "2222"
        self.assertTrue(cache.canReadFromCache())

    def testCacheSubdir(self):
        attach = Attachment(self.testPage)

        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # После того, как один раз сгенерили страницу, если ничего не
        # изменилось, можно кешировать
        self.assertTrue(cache.canReadFromCache())

        # Добавим файл в dir
        with open(os.path.join(attach.getAttachPath(), "dir", "temp.tmp"), "w") as fp:
            fp.write("bla-bla-bla")

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # Добавим еще одну вложенную директорию
        subdir = os.path.join(attach.getAttachPath(), "dir", "subdir_2")
        os.mkdir(subdir)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # Добавим файл в dir/subdir_2
        with open(os.path.join(subdir, "temp2.tmp"), "w") as fp:
            fp.write("bla-bla-bla")

        self.assertFalse(cache.canReadFromCache())

    def testCacheSubpages(self):
        """
        Проверка кэширования при добавлении новых подстраниц
        """
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

        # Добавляем новую подстраницу
        WikiPageFactory().create(self.testPage, "Подстраница 1", [])
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

    def testCacheStyle(self):
        """
        Проверка на то, что изменение стиля страницы сбрасывает кэш
        """
        style = Style()

        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        exampleStyleDir = "../test/styles/example_jblog/example_jblog"
        exampleStyleDir2 = "../test/styles/example_jnet/example_jnet"

        # Изменим стиль страницы
        style.setPageStyle(self.testPage, exampleStyleDir)

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        # Еще раз изменим стиль
        style.setPageStyle(self.testPage, exampleStyleDir2)

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        # Установим стиль по умолчанию
        style.setPageStyleDefault(self.testPage)

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

    def testCacheLoadPlugins1(self):
        """
        Проверка на то, что при изменении списка установленных плагинов не работает кэширование
        """
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        # После того, как один раз сгенерили страницу, если ничего не
        # изменилось, можно кешировать
        self.assertTrue(cache.canReadFromCache())

        # Загрузили плагин. Кэш не должен сработать
        self.application.plugins.load(["../test/plugins/testempty1"])
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # Загрузили еще один плагин
        self.application.plugins.load(["../test/plugins/testempty2"])
        self.assertFalse(cache.canReadFromCache())

    def testCacheLoadPlugins2(self):
        """
        Проверка на то, что при изменении списка установленных плагинов не работает кэширование
        """
        self.application.plugins.clear()
        self.application.plugins.load(["../test/plugins/testempty1"])
        self.application.plugins.load(["../test/plugins/testempty2"])

        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        self.application.plugins.clear()

        self.assertFalse(cache.canReadFromCache())

        # Перезагрузим плагины в другом порядке
        self.application.plugins.load(["../test/plugins/testempty2"])
        self.application.plugins.load(["../test/plugins/testempty1"])

        self.assertEqual(len(self.application.plugins), 2)
        self.assertTrue(cache.canReadFromCache())
        self.application.plugins.clear()

    def testConfigThumbSizeCache(self):
        """
        Тест на то, что на кэширование влияет изменение размера превьюшки по умолчанию
        """
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        # После того, как один раз сгенерили страницу, если ничего не
        # изменилось, можно кешировать
        self.assertTrue(cache.canReadFromCache())

        self.application.config.set(
            WikiConfig.WIKI_SECTION,
            WikiConfig.THUMB_SIZE_PARAM,
            WikiConfig.THUMB_SIZE_DEFAULT + 100)

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        self.application.config.set(
            WikiConfig.WIKI_SECTION,
            WikiConfig.THUMB_SIZE_PARAM,
            "Бла-бла-бла")
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.application.config.set(
            WikiConfig.WIKI_SECTION,
            WikiConfig.THUMB_SIZE_PARAM,
            WikiConfig.THUMB_SIZE_DEFAULT)
        self.assertTrue(cache.canReadFromCache())

    def testConfigFontNameCache(self):
        """
        Тест на то, что на кэширование влияет изменение размера превьюшки по умолчанию
        """
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        # После того, как один раз сгенерили страницу, если ничего не
        # изменилось, можно кешировать
        self.assertTrue(cache.canReadFromCache())

        self.application.config.set(HtmlRenderConfig.HTML_SECTION,
                                    HtmlRenderConfig.FONT_FACE_NAME_PARAM,
                                    "Бла-бла-бла")

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

    def testResetHash1(self):
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # После того, как один раз сгенерили страницу, если ничего не
        # изменилось, можно кешировать
        self.assertTrue(cache.canReadFromCache())

        cache.resetHash()
        self.assertFalse(cache.canReadFromCache())

    def testResetHash2(self):
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache(self.testPage, self.application)

        self.assertFalse(cache.canReadFromCache())
        cache.resetHash()

        cache.saveHash()

        # После того, как один раз сгенерили страницу, если ничего не
        # изменилось, можно кешировать
        self.assertTrue(cache.canReadFromCache())

        cache.resetHash()
        self.assertFalse(cache.canReadFromCache())

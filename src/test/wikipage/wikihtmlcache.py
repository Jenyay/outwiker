# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.core.defines import PAGE_RESULT_HTML

from outwiker.gui.guiconfig import HtmlRenderConfig

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlcache import HtmlCache
from outwiker.pages.wiki.emptycontent import EmptyContent
from outwiker.pages.wiki.wikiconfig import WikiConfig

from test.utils import removeDir


class WikiHtmlCacheTest (unittest.TestCase):
    def setUp(self):
        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        files = [u"image.jpg", u"dir"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        self.attach_page2 = Attachment (self.wikiroot[u"Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)

        self.wikitext = u"""Бла-бла-бла
        %thumb maxsize=250%Attach:image.jpg%%
        Бла-бла-бла"""

        self.testPage.content = self.wikitext

        self.__htmlconfig = HtmlRenderConfig (Application.config)
        self.__setDefaultConfig()

        self.resultPath = os.path.join (self.testPage.path, PAGE_RESULT_HTML)


    def __setDefaultConfig (self):
        # Установим размер превьюшки, не совпадающий с размером по умолчанию
        Application.config.set (WikiConfig.WIKI_SECTION,
                                WikiConfig.THUMB_SIZE_PARAM,
                                WikiConfig.THUMB_SIZE_DEFAULT)

        Application.config.set (HtmlRenderConfig.HTML_SECTION,
                                HtmlRenderConfig.FONT_FACE_NAME_PARAM,
                                HtmlRenderConfig.FONT_NAME_DEFAULT)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def tearDown(self):
        self.__setDefaultConfig()
        removeDir (self.path)


    def testCache1 (self):
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        cache.saveHash()
        self.assertTrue (cache.canReadFromCache())

        self.testPage.content = u"бла-бла-бла"

        # Изменили содержимое страницы, опять нельзя кешировать
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue (cache.canReadFromCache())

        # Добавим файл
        attach = Attachment (self.testPage)
        attach.attach ([os.path.join (self.filesPath, u"add.png")])

        self.assertFalse (cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue (cache.canReadFromCache())


    def testCacheRename (self):
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (cache.canReadFromCache())

        self.testPage.content = u"бла-бла-бла"

        # Изменили содержимое страницы, опять нельзя кешировать
        self.assertFalse (cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue (cache.canReadFromCache())

        # Изменили заголовок
        self.testPage.title = u"Новый заголовок"

        self.assertFalse (cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue (cache.canReadFromCache())


    def testCacheEmpty (self):
        emptycontent = EmptyContent (Application.config)
        self.testPage.content = u""

        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)

        self.assertFalse (cache.canReadFromCache())
        cache.saveHash()

        # Страница пустая, изменился шаблон для путой записи
        emptycontent.content = u"1111"
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        # Изменилось содержимое страницы
        self.testPage.content = u"Бла-бла-бла"
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue (cache.canReadFromCache())
        cache.saveHash()

        # Изменился шаблон страницы, но страница уже не пустая
        emptycontent.content = u"2222"
        self.assertTrue (cache.canReadFromCache())


    def testCacheSubdir (self):
        attach = Attachment (self.testPage)

        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (cache.canReadFromCache())

        # Добавим файл в dir
        with open (os.path.join (attach.getAttachPath(), "dir", "temp.tmp"), "w") as fp:
            fp.write ("bla-bla-bla")

        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        # Добавим еще одну вложенную директорию
        subdir = os.path.join (attach.getAttachPath(), "dir", "subdir_2")
        os.mkdir (subdir)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        # Добавим файл в dir/subdir_2
        with open (os.path.join (subdir, "temp2.tmp"), "w") as fp:
            fp.write ("bla-bla-bla")

        self.assertFalse (cache.canReadFromCache())


    def testCacheSubpages (self):
        """
        Проверка кэширования при добавлении новых подстраниц
        """
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue (cache.canReadFromCache())

        # Добавляем новую подстраницу
        WikiPageFactory().create (self.testPage, u"Подстраница 1", [])
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue (cache.canReadFromCache())


    def testCacheStyle (self):
        """
        Проверка на то, что изменение стиля страницы сбрасывает кэш
        """
        style = Style()

        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue (cache.canReadFromCache())

        exampleStyleDir = u"../test/styles/example_jblog/example_jblog"
        exampleStyleDir2 = u"../test/styles/example_jnet/example_jnet"

        # Изменим стиль страницы
        style.setPageStyle (self.testPage, exampleStyleDir)

        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue (cache.canReadFromCache())

        # Еще раз изменим стиль
        style.setPageStyle (self.testPage, exampleStyleDir2)

        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue (cache.canReadFromCache())

        # Установим стиль по умолчанию
        style.setPageStyleDefault (self.testPage)

        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue (cache.canReadFromCache())


    def testCacheLoadPlugins1 (self):
        """
        Проверка на то, что при изменении списка установленных плагинов не работает кэширование
        """
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (cache.canReadFromCache())

        # Загрузили плагин. Кэш не должен сработать
        Application.plugins.load ([u"../plugins/testempty1"])
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        # Загрузили еще один плагин
        Application.plugins.load ([u"../plugins/testempty2"])
        self.assertFalse (cache.canReadFromCache())


    def testCacheLoadPlugins2 (self):
        """
        Проверка на то, что при изменении списка установленных плагинов не работает кэширование
        """
        Application.plugins.clear()
        Application.plugins.load ([u"../plugins/testempty1"])
        Application.plugins.load ([u"../plugins/testempty2"])

        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        Application.plugins.clear()

        self.assertFalse (cache.canReadFromCache())

        # Перезагрузим плагины в другом порядке
        Application.plugins.load ([u"../plugins/testempty2"])
        Application.plugins.load ([u"../plugins/testempty1"])

        self.assertEqual (len (Application.plugins), 2)
        self.assertTrue (cache.canReadFromCache())
        Application.plugins.clear()


    def testConfigThumbSizeCache (self):
        """
        Тест на то, что на кэширование влияет изменение размера превьюшки по умолчанию
        """
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (cache.canReadFromCache())

        Application.config.set (WikiConfig.WIKI_SECTION, WikiConfig.THUMB_SIZE_PARAM, WikiConfig.THUMB_SIZE_DEFAULT + 100)

        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue (cache.canReadFromCache())

        Application.config.set (WikiConfig.WIKI_SECTION, WikiConfig.THUMB_SIZE_PARAM, u"Бла-бла-бла")
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        Application.config.set (WikiConfig.WIKI_SECTION, WikiConfig.THUMB_SIZE_PARAM, WikiConfig.THUMB_SIZE_DEFAULT)
        self.assertTrue (cache.canReadFromCache())


    def testConfigFontNameCache (self):
        """
        Тест на то, что на кэширование влияет изменение размера превьюшки по умолчанию
        """
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (cache.canReadFromCache())

        Application.config.set (HtmlRenderConfig.HTML_SECTION,
                                HtmlRenderConfig.FONT_FACE_NAME_PARAM,
                                u"Бла-бла-бла")

        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue (cache.canReadFromCache())


    def testResetHash1 (self):
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)
        self.assertFalse (cache.canReadFromCache())

        cache.saveHash()

        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (cache.canReadFromCache())

        cache.resetHash()
        self.assertFalse (cache.canReadFromCache())


    def testResetHash2 (self):
        # Только создали страницу, кешировать нельзя
        cache = HtmlCache (self.testPage, Application)

        self.assertFalse (cache.canReadFromCache())
        cache.resetHash()

        cache.saveHash()

        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (cache.canReadFromCache())

        cache.resetHash()
        self.assertFalse (cache.canReadFromCache())

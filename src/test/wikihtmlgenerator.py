#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
import time

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.config import Config
from outwiker.core.style import Style
from outwiker.gui.guiconfig import HtmlRenderConfig

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.pages.wiki.emptycontent import EmptyContent
from outwiker.pages.wiki.wikiconfig import WikiConfig

from utils import removeWiki


class WikiHtmlGeneratorTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "866"

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()
        
        files = [u"image.jpg", u"dir"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        self.attach_page2 = Attachment (self.rootwiki[u"Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)

        self.wikitext = u"""Бла-бла-бла
%thumb maxsize=250%Attach:image.jpg%%
Бла-бла-бла"""

        self.testPage.content = self.wikitext
        
        self.__htmlconfig = HtmlRenderConfig (Application.config)
        self.__setDefaultConfig()


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
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
        self.testPage = self.rootwiki[u"Страница 2"]
        

    def tearDown(self):
        self.__setDefaultConfig()
        removeWiki (self.path)


    def test1 (self):
        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml ()

        self.assertEqual (htmlpath, os.path.join (self.testPage.path, u"__content.html"))
        self.assertTrue (os.path.exists (htmlpath))


    def testCache1 (self):
        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (generator.canReadFromCache())

        self.testPage.content = u"бла-бла-бла"

        # Изменили содержимое страницы, опять нельзя кешировать
        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())

        # Добавим файл
        attach = Attachment (self.testPage)
        attach.attach ([os.path.join (self.filesPath, u"add.png")])

        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())


    def testCache2 (self):
        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)

        path = generator.makeHtml ()
        ftime = os.stat(path).st_mtime
        time.sleep (0.1)

        path2 = generator.makeHtml ()
        ftime2 = os.stat(path).st_mtime

        self.assertEqual (ftime, ftime2)
        time.sleep (0.1)

        # Изменили содержимое страницы, опять нельзя кешировать
        self.testPage.content = u"бла-бла-бла"
        path3 = generator.makeHtml ()
        ftime3 = os.stat(path).st_mtime

        self.assertNotEqual (ftime2, ftime3)
        time.sleep (0.1)

        path4 = generator.makeHtml ()
        ftime4 = os.stat(path).st_mtime

        self.assertEqual (ftime3, ftime4)
        time.sleep (0.1)

        # Добавим файл
        attach = Attachment (self.testPage)
        attach.attach ([os.path.join (self.filesPath, u"add.png")])

        path5 = generator.makeHtml ()
        ftime5 = os.stat(path).st_mtime

        self.assertNotEqual (ftime4, ftime5)
        time.sleep (0.1)

        path6 = generator.makeHtml ()
        ftime6 = os.stat(path).st_mtime

        self.assertEqual (ftime5, ftime6)


    def testCacheRename (self):
        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (generator.canReadFromCache())

        self.testPage.content = u"бла-бла-бла"

        # Изменили содержимое страницы, опять нельзя кешировать
        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())

        # Изменили заголовок
        self.testPage.title = u"Новый заголовок"

        # Добавим файл
        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())


    def testCacheEmpty1 (self):
        emptycontent = EmptyContent (Application.config)
        self.testPage.content = u""

        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()

        # Страница пустая, изменился шаблон для путой записи
        emptycontent.content = u"1111"
        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()

        # Изменилось содержимое страницы
        self.testPage.content = u"Бла-бла-бла"
        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()

        self.assertTrue (generator.canReadFromCache())
        generator.makeHtml ()

        # Изменился шаблон страницы, но страница уже не пустая
        emptycontent.content = u"2222"
        self.assertTrue (generator.canReadFromCache())


    def testCacheSubdir (self):
        attach = Attachment (self.testPage)

        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (generator.canReadFromCache())

        # Добавим файл в dir
        with open (os.path.join (attach.getAttachPath(), "dir", "temp.tmp"), "w" ) as fp:
            fp.write ("bla-bla-bla")

        self.assertFalse (generator.canReadFromCache())

        # Добавим еще одну вложенную директорию
        subdir = os.path.join (attach.getAttachPath(), "dir", "subdir_2")
        os.mkdir (subdir)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()

        # Добавим файл в dir/subdir_2
        with open (os.path.join (subdir, "temp2.tmp"), "w" ) as fp:
            fp.write ("bla-bla-bla")

        self.assertFalse (generator.canReadFromCache())


    def testCacheSubpages (self):
        """
        Проверка кэширования при добавлении новых подстраниц
        """
        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())

        # Добавляем новую подстраницу
        WikiPageFactory.create (self.testPage, u"Подстраница 1", [])
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())


    def testCacheStyle (self):
        """
        Проверка на то, что изменение стиля страницы сбрасывает кэш
        """
        style = Style()

        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())

        exampleStyleDir = u"../test/styles/example_jblog/example_jblog"
        exampleStyleDir2 = u"../test/styles/example_jnet/example_jnet"

        # Изменим стиль страницы
        style.setPageStyle (self.testPage, exampleStyleDir)

        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())

        # Еще раз изменим стиль
        style.setPageStyle (self.testPage, exampleStyleDir2)

        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())

        # Изменим стиль на тот же 
        style.setPageStyle (self.testPage, exampleStyleDir2)
        self.assertTrue (generator.canReadFromCache())

        # Установим стиль по умолчанию
        style.setPageStyleDefault (self.testPage)

        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())


    def testEmpty1 (self):
        text = u"бла-бла-бла"

        content = EmptyContent (Application.config)
        content.content = text

        # Очистим содержимое, чтобы использовать EmptyContent
        self.testPage.content = u""

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml()

        # Проверим, что в результирующем файле есть содержимое text
        with open (htmlpath) as fp:
            result = unicode (fp.read(), "utf8")

        self.assertTrue (text in result)


    def testEmpty2 (self):
        text = u"(:attachlist:)"

        content = EmptyContent (Application.config)
        content.content = text

        # Очистим содержимое, чтобы использовать EmptyContent
        self.testPage.content = u""

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml()

        # Проверим, что в результирующем файле есть содержимое text
        with open (htmlpath) as fp:
            result = unicode (fp.read(), "utf8")

        self.assertTrue (u"image.jpg" in result)


    def testCacheLoadPlugins1 (self):
        """
        Проверка на то, что при изменении списка установленных плагинов не работает кэширование
        """
        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (generator.canReadFromCache())

        # Загрузили плагин. Кэш не должен сработать
        Application.plugins.load ([u"../plugins/testempty1"])
        self.assertFalse (generator.canReadFromCache())

        # Загрузили еще один плагин
        Application.plugins.load ([u"../plugins/testempty2"])
        self.assertFalse (generator.canReadFromCache())


    def testCacheLoadPlugins2 (self):
        """
        Проверка на то, что при изменении списка установленных плагинов не работает кэширование
        """
        Application.plugins.clear()
        Application.plugins.load ([u"../plugins/testempty1"])
        Application.plugins.load ([u"../plugins/testempty2"])

        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()

        Application.plugins.clear()

        self.assertFalse (generator.canReadFromCache())
        
        # Перезагрузим плагины в другом порядке
        Application.plugins.load ([u"../plugins/testempty1"])
        Application.plugins.load ([u"../plugins/testempty2"])

        self.assertEqual (len (Application.plugins), 2)
        self.assertTrue (generator.canReadFromCache())


    def testConfigThumbSizeCache (self):
        """
        Тест на то, что на кэширование влияет изменение размера превьюшки по умолчанию
        """
        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (generator.canReadFromCache())

        Application.config.set (WikiConfig.WIKI_SECTION, WikiConfig.THUMB_SIZE_PARAM, WikiConfig.THUMB_SIZE_DEFAULT + 100)

        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())

        Application.config.set (WikiConfig.WIKI_SECTION, WikiConfig.THUMB_SIZE_PARAM, u"Бла-бла-бла")
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        Application.config.set (WikiConfig.WIKI_SECTION, WikiConfig.THUMB_SIZE_PARAM, WikiConfig.THUMB_SIZE_DEFAULT)
        self.assertTrue (generator.canReadFromCache())


    def testConfigFontNameCache (self):
        """
        Тест на то, что на кэширование влияет изменение размера превьюшки по умолчанию
        """
        # Только создали страницу, кешировать нельзя
        generator = HtmlGenerator (self.testPage)
        self.assertFalse (generator.canReadFromCache())

        generator.makeHtml ()
        # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
        self.assertTrue (generator.canReadFromCache())

        Application.config.set (HtmlRenderConfig.HTML_SECTION, 
                HtmlRenderConfig.FONT_FACE_NAME_PARAM, 
                u"Бла-бла-бла")

        self.assertFalse (generator.canReadFromCache())
        generator.makeHtml ()
        self.assertTrue (generator.canReadFromCache())


    # def testFontNameInvalidEncoding (self):
    #     """
    #     Тест на то, что на кэширование влияет изменение размера превьюшки по умолчанию
    #     """
    #     Application.config.set (HtmlRenderConfig.HTML_SECTION, 
    #             HtmlRenderConfig.FONT_FACE_NAME_PARAM, 
    #             u"Arial")

    #     # Только создали страницу, кешировать нельзя
    #     generator = HtmlGenerator (self.testPage)
    #     self.assertFalse (generator.canReadFromCache())

    #     generator.makeHtml ()
    #     # После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
    #     self.assertTrue (generator.canReadFromCache())

    #     fontname = u"Бла-бла-бла"

    #     Application.config.set (HtmlRenderConfig.HTML_SECTION, 
    #             HtmlRenderConfig.FONT_FACE_NAME_PARAM, 
    #             fontname.encode ("cp1251"))

    #     self.assertFalse (generator.canReadFromCache())
    #     generator.makeHtml ()
    #     self.assertTrue (generator.canReadFromCache())

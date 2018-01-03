# -*- coding: utf-8 -*-

import os
import html
import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserLinkTest(unittest.TestCase):
    def setUp(self):
        self.encoding = "866"

        self.filesPath = "../test/samplefiles/"

        self.url1 = "http://example.com"
        self.url2 = "http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"
        self.urlimage = "http://example.com/image.png"

        self.pagelinks = ["Страница 1", "/Страница 1", "/Страница 2/Страница 3"]
        self.pageComments = ["Страницо 1", "Страницо 1", "Страницо 3"]

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = WikiPageFactory()
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "#Страница3", [])
        factory.create(self.wikiroot["Страница 2"], "# Страница 4", [])
        self.testPage = self.wikiroot["Страница 2"]

        files = ["accept.png", "add.png", "anchor.png", "filename.tmp",
                 "файл с пробелами.tmp", "картинка с пробелами.png",
                 "image.jpg", "image.jpeg", "image.png", "image.tif", "image.tiff", "image.gif",
                 "image_01.JPG", "dir", "dir.xxx", "dir.png"]

        fullFilesPath = [os.path.join(self.filesPath, fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

    def tearDown(self):
        removeDir(self.path)

    def testUrl1(self):
        text = "бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (self.url1)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrl2(self):
        text = "бла-бла-бла \ntest %s бла-бла-бла\nбла-бла-бла" % (self.url2)
        result = 'бла-бла-бла \ntest <a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url2, self.url2)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink1(self):
        text = "бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (self.url1)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink2(self):
        text = "бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (self.url2)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url2, html.escape(self.url2))

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink3(self):
        url = "http://jenyay.net/social/feed.png"

        text = "бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (url)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (url, url)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink4(self):
        text = "[[http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431 | Ссылко]]"
        result = '<a href="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">Ссылко</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink5(self):
        text = "[[Ссылко -> http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431]]"
        result = '<a href="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">Ссылко</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink6(self):
        text = "[[\\t -> http://www.example.com]]"
        result = '<a href="http://www.example.com">\\t</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink7(self):
        text = "[[http://www.example.com | \\t]]"
        result = '<a href="http://www.example.com">\\t</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink8(self):
        text = "[[\\t]]"
        result = '<a href="\\t">\\t</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink3(self):
        comment = "Ссылко с '''полужирным''' текстом"
        text = "бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url2, "Ссылко с <b>полужирным</b> текстом")

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink4(self):
        comment = "Ссылко с '''полужирным''' текстом"
        text = "бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url2, "Ссылко с <b>полужирным</b> текстом")

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink5(self):
        text = "бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (self.url1, self.url1)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink6(self):
        text = "бла-бла-бла \n[[Комментарий с <, > и & -> %s]] бла-бла-бла\nбла-бла-бла" % (self.url1)
        result = 'бла-бла-бла \n<a href="%s">Комментарий с &lt;, &gt; и &amp;</a> бла-бла-бла\nбла-бла-бла' % (self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink7(self):
        text = "бла-бла-бла \n[[%s | Комментарий с <, > и &]] бла-бла-бла\nбла-бла-бла" % (self.url1)
        result = 'бла-бла-бла \n<a href="%s">Комментарий с &lt;, &gt; и &amp;</a> бла-бла-бла\nбла-бла-бла' % (self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testStrikeLink1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{-%s-} -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><strike>%s</strike></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testStrikeLink2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | {-%s-}]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><strike>%s</strike></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testPageLinks(self):
        for link in self.pagelinks:
            text = "бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (link)
            result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (link, link)

            self.assertEqual(self.parser.toHtml(text), result)

    def testPageLinkSharp1(self):
        """
        Проверка ссылок на страницы с #
        """
        text = "бла-бла-бла \n[[#Страница3]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a href="#Страница3">#Страница3</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testPageLinkSharp2(self):
        """
        Проверка ссылок на страницы с #
        """
        text = "бла-бла-бла \n[[# Страница 4]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a href="# Страница 4"># Страница 4</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testAnchor1(self):
        """
        Проверка создания якорей
        """
        text = "бла-бла-бла \n[[#anchor]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a id="anchor"></a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testAnchor2(self):
        """
        Проверка создания якорей
        """
        text = "бла-бла-бла \n[[#якорь]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a id="якорь"></a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testNoFormatLinks1(self):
        for link in self.pagelinks:
            text = "бла-бла-бла \n[[%s | [='''ля-ля-ля'''=] ]] бла-бла-бла\nбла-бла-бла" % (link)
            result = "бла-бла-бла \n<a href=\"%s\">'''ля-ля-ля'''</a> бла-бла-бла\nбла-бла-бла" % (link)

            self.assertEqual(self.parser.toHtml(text), result)

    def testNoFormatLinks2(self):
        for link in self.pagelinks:
            text = "бла-бла-бла \n[[[='''ля-ля-ля'''=] -> %s]] бла-бла-бла\nбла-бла-бла" % (link)
            result = "бла-бла-бла \n<a href=\"%s\">'''ля-ля-ля'''</a> бла-бла-бла\nбла-бла-бла" % (link)

            self.assertEqual(self.parser.toHtml(text), result)

    def testPageCommentsLinks1(self):
        for n in range(len(self.pagelinks)):
            link = self.pagelinks[n]
            comment = self.pageComments[n]

            text = "бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (link, comment)
            result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (link, comment)

            self.assertEqual(self.parser.toHtml(text), result)

    def testPageCommentsLinks2(self):
        for n in range(len(self.pagelinks)):
            link = self.pagelinks[n]
            comment = self.pageComments[n]

            text = "бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, link)
            result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (link, comment)

            self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSubscript1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | '_%s_']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><sub>%s</sub></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSubscript2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['_%s_' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><sub>%s</sub></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSuperscript1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | '^%s^']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><sup>%s</sup></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSuperscript2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['^%s^' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><sup>%s</sup></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBoldItalic1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | ''''%s'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><b><i>%s</i></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBoldItalic2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[''''%s'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><b><i>%s</i></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBold1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | '''%s''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><b>%s</b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBold2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['''%s''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><b>%s</b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkItalic1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | ''%s'']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><i>%s</i></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkItalic2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[''%s'' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><i>%s</i></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage1(self):
        text = "бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (self.urlimage)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.urlimage, self.urlimage)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.urlimage)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.urlimage, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage3(self):
        text = "бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (self.urlimage, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><img src="%s"/></a> бла-бла-бла\nбла-бла-бла' % (self.url2, self.urlimage)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage4(self):
        text = "бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (self.url2, self.urlimage)
        result = 'бла-бла-бла \n<a href="%s"><img src="%s"/></a> бла-бла-бла\nбла-бла-бла' % (self.url2, self.urlimage)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkUnderline1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | {+%s+}]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><u>%s</u></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkUnderline2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{+%s+} -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><u>%s</u></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | ''''_%s_'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><b><sub>%s</sub></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''_%s_'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><b><sub>%s</sub></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc3(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | ''''^%s^'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><b><sup>%s</sup></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc4(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''^%s^'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><b><sup>%s</sup></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc5(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | '''_%s_''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><i><sub>%s</sub></i></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc6(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ '''_%s_''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><i><sub>%s</sub></i></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc7(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | '''^%s^''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><i><sup>%s</sup></i></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc8(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ '''^%s^''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><i><sup>%s</sup></i></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc9(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | ''''%s'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><b><i>%s</i></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc10(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''%s'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><b><i>%s</i></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc11(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[%s | ''''%s'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = 'бла-бла-бла \n<a href="%s"><b><i>%s</i></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc12(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''%s'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s"><b><i>%s</i></b></a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testFileAttach(self):
        comment = "Attach:filename.tmp"
        text = "бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = 'бла-бла-бла \n<a href="%s">%s</a> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testManyArrows(self):
        text = "бла-бла-бла \n[[Бла-бла-бла -> Бла-бла-бла -> http://jenyay.net]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a href="http://jenyay.net">Бла-бла-бла -&gt; Бла-бла-бла</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testManyPipes1(self):
        text = "бла-бла-бла \n[[http://jenyay.net | Бла-бла-бла | Бла-бла-бла]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a href="http://jenyay.net">Бла-бла-бла | Бла-бла-бла</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testManyPipes2(self):
        text = "бла-бла-бла \n[[http://jenyay.net/|blablabla | Бла-бла-бла]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a href="http://jenyay.net/|blablabla">Бла-бла-бла</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testManyPipes3(self):
        text = "бла-бла-бла \n[[http://jenyay.net/|blablabla|Бла-бла-бла]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a href="http://jenyay.net/|blablabla">Бла-бла-бла</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

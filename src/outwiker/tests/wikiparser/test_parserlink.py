# -*- coding: utf-8 -*-

import os
import html
import unittest
from tempfile import mkdtemp

from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.utils import removeDir


class ParserLinkTest(unittest.TestCase):
    def setUp(self):
        self.filesPath = "testdata/samplefiles/"

        self.url1 = "http://example.com"
        self.url2 = "http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"
        self.urlimage = "http://example.com/image.png"

        self.pagelinks = [
            "Страница 1",
            "/Страница 1",
            "/Страница 2/Страница 3"]
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
        factory.create(self.wikiroot["Страница 2"], "Страница3", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 4", [])
        self.testPage = self.wikiroot["Страница 2"]

        files = ["accept.png", "filename.tmp",
                 "файл с пробелами.tmp", "картинка с пробелами.png",
                 "dir"]

        fullFilesPath = [
            os.path.join(
                self.filesPath,
                fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

    def tearDown(self):
        removeDir(self.path)

    def testUrl1(self):
        text = "бла-бла-бла \n{} бла-бла-бла\nбла-бла-бла".format(self.url1)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1, self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrl2(self):
        text = "бла-бла-бла \ntest {} бла-бла-бла\nбла-бла-бла".format(
            self.url2)
        result = 'бла-бла-бла \ntest <a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, self.url2)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink1(self):
        text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(
            self.url1)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1, self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink2(self):
        text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, html.escape(self.url2))

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink3(self):
        url = "http://jenyay.net/social/feed.png"

        text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(url)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            url, url)

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
        result = '<a class="ow-link ow-link-page" href="page://\\t">\\t</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink3(self):
        comment = "Ссылко с '''полужирным''' текстом"
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, "Ссылко с <b>полужирным</b> текстом")

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink4(self):
        comment = "Ссылко с '''полужирным''' текстом"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, "Ссылко с <b>полужирным</b> текстом")

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink5(self):
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url1, self.url1)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1, self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink6(self):
        text = "бла-бла-бла \n[[Комментарий с <, > и & -> {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url1)
        result = 'бла-бла-бла \n<a href="{}">Комментарий с &lt;, &gt; и &amp;</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink7(self):
        text = "бла-бла-бла \n[[{} | Комментарий с <, > и &]] бла-бла-бла\nбла-бла-бла".format(
            self.url1)
        result = 'бла-бла-бла \n<a href="{}">Комментарий с &lt;, &gt; и &amp;</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1)

        self.assertEqual(self.parser.toHtml(text), result)

    def testStrikeLink1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{{-{}-}} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><strike>{}</strike></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testStrikeLink2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | {{-{}-}}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><strike>{}</strike></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testPageLinks(self):
        for link in self.pagelinks:
            text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(link)
            result = 'бла-бла-бла \n<a class="ow-link ow-link-page" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                link, link)

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
            text = "бла-бла-бла \n[[{} | [='''ля-ля-ля'''=] ]] бла-бла-бла\nбла-бла-бла".format(
                link)
            result = "бла-бла-бла \n<a class=\"ow-link ow-link-page\" href=\"page://{}\">'''ля-ля-ля'''</a> бла-бла-бла\nбла-бла-бла".format(
                link)

            self.assertEqual(self.parser.toHtml(text), result)

    def testNoFormatLinks2(self):
        for link in self.pagelinks:
            text = "бла-бла-бла \n[[[='''ля-ля-ля'''=] -> {}]] бла-бла-бла\nбла-бла-бла".format(
                link)
            result = "бла-бла-бла \n<a class=\"ow-link ow-link-page\" href=\"page://{}\">'''ля-ля-ля'''</a> бла-бла-бла\nбла-бла-бла".format(
                link)

            self.assertEqual(self.parser.toHtml(text), result)

    def testPageCommentsLinks1(self):
        for n in range(len(self.pagelinks)):
            link = self.pagelinks[n]
            comment = self.pageComments[n]

            text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
                link, comment)
            result = 'бла-бла-бла \n<a class="ow-link ow-link-page" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                link, comment)

            self.assertEqual(self.parser.toHtml(text), result)

    def testPageCommentsLinks2(self):
        for n in range(len(self.pagelinks)):
            link = self.pagelinks[n]
            comment = self.pageComments[n]

            text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
                comment, link)
            result = 'бла-бла-бла \n<a class="ow-link ow-link-page" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                link, comment)

            self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSubscript1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '_{}_']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><sub>{}</sub></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSubscript2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['_{}_' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><sub>{}</sub></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSuperscript1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '^{}^']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><sup>{}</sup></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSuperscript2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['^{}^' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><sup>{}</sup></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBoldItalic1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''{}'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBoldItalic2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[''''{}'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBold1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '''{}''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><b>{}</b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBold2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['''{}''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><b>{}</b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkItalic1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''{}'']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><i>{}</i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkItalic2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[''{}'' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><i>{}</i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage1(self):
        text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(
            self.urlimage)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.urlimage, self.urlimage)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.urlimage)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.urlimage, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage3(self):
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            self.urlimage, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><img class="ow-image" src="{}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, self.urlimage)

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage4(self):
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, self.urlimage)
        result = 'бла-бла-бла \n<a href="{}"><img class="ow-image" src="{}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, self.urlimage)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkUnderline1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | {{+{}+}}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><u>{}</u></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkUnderline2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{{+{}+}} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><u>{}</u></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''_{}_'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><b><sub>{}</sub></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''_{}_'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><b><sub>{}</sub></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc3(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''^{}^'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><b><sup>{}</sup></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc4(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''^{}^'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><b><sup>{}</sup></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc5(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '''_{}_''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><i><sub>{}</sub></i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc6(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ '''_{}_''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><i><sub>{}</sub></i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc7(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '''^{}^''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><i><sup>{}</sup></i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc8(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ '''^{}^''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><i><sup>{}</sup></i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc9(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''{}'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc10(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''{}'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc11(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''{}'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc12(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''{}'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachArrow(self):
        comment = "Attach:filename.tmp"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachArrowSingleQuotes(self):
        comment = "Attach:'filename.tmp'"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachArrowDoubleQuotes(self):
        comment = 'Attach:"filename.tmp"'
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachPipe(self):
        comment = "Attach:filename.tmp"
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachPipeSingleQuotes(self):
        comment = "Attach:'filename.tmp'"
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachPipeDoubleQuotes(self):
        comment = '"Attach:"filename.tmp"'
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment)
        result = 'бла-бла-бла \n<a href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment)

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

    def testMailto_01(self):
        text = "[[mailto:example@example.com | example@example.com]]"
        result = '<a href="mailto:example@example.com">example@example.com</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testMailto_02(self):
        text = "[[example@example.com -> mailto:example@example.com]]"
        result = '<a href="mailto:example@example.com">example@example.com</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testMailto_03(self):
        text = "[[mailto:example@example.com]]"
        result = '<a href="mailto:example@example.com">mailto:example@example.com</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkAttachSimple(self):
        filename = 'filename.tmp'
        text = '[[Attach:{}]]'.format(filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{filename}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachSimpleDoubleQuotes(self):
        filename = 'filename.tmp'
        text = '[[Attach:"{}"]]'.format(filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{filename}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachSimpleSingleQuotes(self):
        filename = 'filename.tmp'
        text = "[[Attach:'{}']]".format(filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{filename}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrow(self):
        filename = 'filename.tmp'
        comment = "bla bla bla"
        text = '[[{comment} -> Attach:{filename}]]'.format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrowDoubleQoutes(self):
        filename = 'filename.tmp'
        comment = "bla bla bla"
        text = '[[{comment} -> Attach:"{filename}"]]'.format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrowSingleQoutes(self):
        filename = 'filename.tmp'
        comment = "bla bla bla"
        text = "[[{comment} -> Attach:'{filename}']]".format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachWithSpacesCommentArrowSingleQoutes(self):
        filename = 'файл с пробелами.tmp'
        comment = "bla bla bla"
        text = "[[{comment} -> Attach:'{filename}']]".format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachWithSpacesCommentArrowDoubleQoutes(self):
        filename = 'файл с пробелами.tmp'
        comment = "bla bla bla"
        text = '[[{comment} -> Attach:"{filename}"]]'.format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipe(self):
        filename = 'filename.tmp'
        comment = "bla bla bla"
        text = '[[Attach:{filename} | {comment}]]'.format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipeDoubleQuotes(self):
        filename = 'filename.tmp'
        comment = "bla bla bla"
        text = '[[Attach:"{filename}" | {comment}]]'.format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipeSingleQuotes(self):
        filename = 'filename.tmp'
        comment = "bla bla bla"
        text = "[[Attach:'{filename}' | {comment}]]".format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachWithSpacesCommentPipeSingleQuotes(self):
        filename = 'файл с пробелами.tmp'
        comment = "bla bla bla"
        text = "[[Attach:'{filename}' | {comment}]]".format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachWithSpacesCommentPipeDoubleQuotes(self):
        filename = 'файл с пробелами.tmp'
        comment = "bla bla bla"
        text = '[[Attach:"{filename}" | {comment}]]'.format(
            comment=comment, filename=filename)
        expected = '<a class="ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageSimple(self):
        filename = 'accept.png'
        text = "бла-бла-бла \n[[Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="{attach_path}">{filename}</a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path, filename=filename)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageSimpleDoublleQuotes(self):
        filename = 'accept.png'
        text = 'бла-бла-бла \n[[Attach:"{filename}"]] бла-бла-бла\nбла-бла-бла'.format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="{attach_path}">{filename}</a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path, filename=filename)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageSimpleSingleQuotes(self):
        filename = 'accept.png'
        text = "бла-бла-бла \n[[Attach:'{filename}']] бла-бла-бла\nбла-бла-бла".format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a class="ow-link-attach ow-attach-file" href="{attach_path}">{filename}</a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path, filename=filename)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageArrow(self):
        filename = 'accept.png'
        text = "бла-бла-бла \n[[Attach:{filename} -> Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a href="{attach_path}"><img class="ow-image" src="{attach_path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageArrowSingleQuotes(self):
        filename = 'accept.png'
        text = "бла-бла-бла \n[[Attach:'{filename}' -> Attach:'{filename}']] бла-бла-бла\nбла-бла-бла".format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a href="{attach_path}"><img class="ow-image" src="{attach_path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageArrowDoubleQuotes(self):
        filename = 'accept.png'
        text = 'бла-бла-бла \n[[Attach:"{filename}" -> Attach:"{filename}"]] бла-бла-бла\nбла-бла-бла'.format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a href="{attach_path}"><img class="ow-image" src="{attach_path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImagePipe(self):
        filename = 'accept.png'
        text = "бла-бла-бла \n[[Attach:{filename} | Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a href="{attach_path}"><img class="ow-image" src="{attach_path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImagePipeSingleQuotes(self):
        filename = 'accept.png'
        text = "бла-бла-бла \n[[Attach:'{filename}' | Attach:'{filename}']] бла-бла-бла\nбла-бла-бла".format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a href="{attach_path}"><img class="ow-image" src="{attach_path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImagePipeDoubleQuotes(self):
        filename = 'accept.png'
        text = 'бла-бла-бла \n[[Attach:"{filename}" | Attach:"{filename}"]] бла-бла-бла\nбла-бла-бла'.format(
            filename=filename)
        attach_path = '{}/{}'.format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a href="{attach_path}"><img class="ow-image" src="{attach_path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path)

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

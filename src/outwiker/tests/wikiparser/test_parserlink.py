# -*- coding: utf-8 -*-

import re
import os
import html
import unittest
from tempfile import mkdtemp
from urllib.parse import quote

from outwiker.api.core.tree import createNotesTree
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.utils import removeDir


class ParserLinkTest(unittest.TestCase):
    def setUp(self):
        self._application = Application()
        self.filesPath = "testdata/samplefiles/"

        self.url1 = "http://example.com"
        self.url2 = (
            "http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"
        )
        self.urlimage = "http://example.com/image.png"

        self._invalid_page_links = ["Отсутствующая страница 1", "/Отсутствующая страница 1", "/Страница 2/Отсутствующая страница 3"]
        self._page_links = ["Страница 2", "/Страница 2", "Страница 2/Страница 3", "/Страница 2/Страница 3"]
        self.pageComments = ["Комментарий 1", "Комментарий 2", "Комментарий 3"]

        self._createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self._application)

    def _createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix="Абырвалг абыр")

        self.wikiroot = createNotesTree(self.path)

        factory = WikiPageFactory()
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 4", [])

        self.testPage = self.wikiroot["Страница 2"]

        files = [
            "accept.png",
            "filename.tmp",
            "файл с пробелами.tmp",
            "картинка с пробелами.png",
            "dir",
        ]

        fullFilesPath = [os.path.join(self.filesPath, fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)
        self._application.wikiroot = self.wikiroot

    def tearDown(self):
        self._application.wikiroot = None
        removeDir(self.path)

    def testUrl1(self):
        text = "бла-бла-бла \n{} бла-бла-бла\nбла-бла-бла".format(self.url1)
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1, self.url1
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrl2(self):
        text = "бла-бла-бла \ntest {} бла-бла-бла\nбла-бла-бла".format(self.url2)
        result = 'бла-бла-бла \ntest <a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, self.url2
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink1(self):
        text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(self.url1)
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1, self.url1
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink2(self):
        text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(self.url2)
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, html.escape(self.url2)
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink3(self):
        url = "http://jenyay.net/social/feed.png"

        text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(url)
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            url, url
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink4(self):
        text = "[[http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431 | Ссылко]]"
        result = '<a class="ow-wiki" href="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">Ссылко</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink5(self):
        text = "[[Ссылко -> http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431]]"
        result = '<a class="ow-wiki" href="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">Ссылко</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink6(self):
        text = "[[\\t -> http://www.example.com]]"
        result = '<a class="ow-wiki" href="http://www.example.com">\\t</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink7(self):
        text = "[[http://www.example.com | \\t]]"
        result = '<a class="ow-wiki" href="http://www.example.com">\\t</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLink8(self):
        text = "[[\\t]]"
        result = '<a class="ow-wiki ow-link-page ow-link-page-error" href="page://{link}">\\t</a>'.format(link=quote("\\t"))

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink3(self):
        comment = "Ссылко с '''полужирным''' текстом"
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, "Ссылко с <b>полужирным</b> текстом"
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink4(self):
        comment = "Ссылко с '''полужирным''' текстом"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, "Ссылко с <b>полужирным</b> текстом"
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink5(self):
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url1, self.url1
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1, self.url1
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink6(self):
        text = "бла-бла-бла \n[[Комментарий с <, > и & -> {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url1
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">Комментарий с &lt;, &gt; и &amp;</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentLink7(self):
        text = "бла-бла-бла \n[[{} | Комментарий с <, > и &]] бла-бла-бла\nбла-бла-бла".format(
            self.url1
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">Комментарий с &lt;, &gt; и &amp;</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url1
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testStrikeLink1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{{-{}-}} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><strike>{}</strike></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testStrikeLink2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | {{-{}-}}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><strike>{}</strike></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testEmptyPageLinks(self):
        for link in self._page_links:
            text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(link)
            expected = 'бла-бла-бла \n<a class="ow-wiki ow-link-page" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                quote(link), link
            )

            result = self.parser.toHtml(text)

            self.assertEqual(result, expected)

    def testEmptyInvalidPageLinks(self):
        for link in self._invalid_page_links:
            text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(link)
            expected = 'бла-бла-бла \n<a class="ow-wiki ow-link-page ow-link-page-error" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                quote(link), link
            )

            result = self.parser.toHtml(text)

            self.assertEqual(result, expected)

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
        for link in self._invalid_page_links:
            text = "бла-бла-бла \n[[{} | [='''ля-ля-ля'''=] ]] бла-бла-бла\nбла-бла-бла".format(
                link
            )
            result = "бла-бла-бла \n<a class=\"ow-wiki ow-link-page ow-link-page-error\" href=\"page://{}\">'''ля-ля-ля'''</a> бла-бла-бла\nбла-бла-бла".format(
                quote(link)
            )

            self.assertEqual(self.parser.toHtml(text), result)

    def testNoFormatLinks2(self):
        for link in self._invalid_page_links:
            text = "бла-бла-бла \n[[[='''ля-ля-ля'''=] -> {}]] бла-бла-бла\nбла-бла-бла".format(
                link
            )
            result = "бла-бла-бла \n<a class=\"ow-wiki ow-link-page ow-link-page-error\" href=\"page://{}\">'''ля-ля-ля'''</a> бла-бла-бла\nбла-бла-бла".format(
                quote(link)
            )

            self.assertEqual(self.parser.toHtml(text), result)

    def testPageLinksWithPipeComment(self):
        for link, comment in zip(self._page_links, self.pageComments):
            text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
                link, comment
            )
            result = 'бла-бла-бла \n<a class="ow-wiki ow-link-page" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                quote(link), comment
            )

            self.assertEqual(self.parser.toHtml(text), result)

    def testInvalidPageLinksWithPipeComment(self):
        for link, comment in zip(self._invalid_page_links, self.pageComments):
            text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
                link, comment
            )
            result = 'бла-бла-бла \n<a class="ow-wiki ow-link-page ow-link-page-error" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                quote(link), comment
            )

            self.assertEqual(self.parser.toHtml(text), result)

    def testPageLinksWithArrowComment(self):
        for link, comment in zip(self._page_links, self.pageComments):
            text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
                comment, link
            )
            result = 'бла-бла-бла \n<a class="ow-wiki ow-link-page" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                quote(link), comment
            )

            self.assertEqual(self.parser.toHtml(text), result)

    def testInvalidPageLinksWithArrowComment(self):
        for link, comment in zip(self._invalid_page_links, self.pageComments):
            text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
                comment, link
            )
            result = 'бла-бла-бла \n<a class="ow-wiki ow-link-page ow-link-page-error" href="page://{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
                quote(link), comment
            )

            self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSubscript1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '_{}_']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><sub>{}</sub></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSubscript2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['_{}_' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><sub>{}</sub></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSuperscript1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '^{}^']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><sup>{}</sup></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkSuperscript2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['^{}^' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><sup>{}</sup></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBoldItalic1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''{}'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBoldItalic2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[''''{}'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBold1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '''{}''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b>{}</b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkBold2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[['''{}''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b>{}</b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkItalic1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''{}'']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><i>{}</i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkItalic2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[''{}'' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><i>{}</i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage1(self):
        text = "бла-бла-бла \n[[{}]] бла-бла-бла\nбла-бла-бла".format(self.urlimage)
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.urlimage, self.urlimage
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.urlimage
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.urlimage, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage3(self):
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            self.urlimage, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><img class="ow-image" src="{}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, self.urlimage
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testUrlImage4(self):
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, self.urlimage
        )
        expected = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><img class="ow-image" src="{}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, self.urlimage
        )

        result = self.parser.toHtml(text)

        self.assertEqual(result, expected, result)

    def testLinkUnderline1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | {{+{}+}}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><u>{}</u></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkUnderline2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{{+{}+}} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><u>{}</u></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc1(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''_{}_'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><sub>{}</sub></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc2(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''_{}_'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><sub>{}</sub></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc3(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''^{}^'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><sup>{}</sup></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc4(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''^{}^'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><sup>{}</sup></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc5(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '''_{}_''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><i><sub>{}</sub></i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc6(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ '''_{}_''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><i><sub>{}</sub></i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc7(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | '''^{}^''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><i><sup>{}</sup></i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc8(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ '''^{}^''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><i><sup>{}</sup></i></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc9(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''{}'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc10(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''{}'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc11(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[{} | ''''{}'''']] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testAdHoc12(self):
        comment = "Ссылко"
        text = "бла-бла-бла \n[[ ''''{}'''' -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}"><b><i>{}</i></b></a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachArrow(self):
        comment = "Attach:filename.tmp"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachArrowSingleQuotes(self):
        comment = "Attach:'filename.tmp'"
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachArrowDoubleQuotes(self):
        comment = 'Attach:"filename.tmp"'
        text = "бла-бла-бла \n[[{} -> {}]] бла-бла-бла\nбла-бла-бла".format(
            comment, self.url2
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachPipe(self):
        comment = "Attach:filename.tmp"
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachPipeSingleQuotes(self):
        comment = "Attach:'filename.tmp'"
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testCommentFileAttachPipeDoubleQuotes(self):
        comment = '"Attach:"filename.tmp"'
        text = "бла-бла-бла \n[[{} | {}]] бла-бла-бла\nбла-бла-бла".format(
            self.url2, comment
        )
        result = 'бла-бла-бла \n<a class="ow-wiki" href="{}">{}</a> бла-бла-бла\nбла-бла-бла'.format(
            self.url2, comment
        )

        self.assertEqual(self.parser.toHtml(text), result)

    def testManyArrows(self):
        text = "бла-бла-бла \n[[Бла-бла-бла -> Бла-бла-бла -> http://jenyay.net]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a class="ow-wiki" href="http://jenyay.net">Бла-бла-бла -&gt; Бла-бла-бла</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testManyPipes1(self):
        text = "бла-бла-бла \n[[http://jenyay.net | Бла-бла-бла | Бла-бла-бла]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a class="ow-wiki" href="http://jenyay.net">Бла-бла-бла | Бла-бла-бла</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testManyPipes2(self):
        text = "бла-бла-бла \n[[http://jenyay.net/|blablabla | Бла-бла-бла]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a class="ow-wiki" href="http://jenyay.net/|blablabla">Бла-бла-бла</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testManyPipes3(self):
        text = "бла-бла-бла \n[[http://jenyay.net/|blablabla|Бла-бла-бла]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<a class="ow-wiki" href="http://jenyay.net/|blablabla">Бла-бла-бла</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), result)

    def testMailto_01(self):
        text = "[[mailto:example@example.com | example@example.com]]"
        result = '<a class="ow-wiki" href="mailto:example@example.com">example@example.com</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testMailto_02(self):
        text = "[[example@example.com -> mailto:example@example.com]]"
        result = '<a class="ow-wiki" href="mailto:example@example.com">example@example.com</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testMailto_03(self):
        text = "[[mailto:example@example.com]]"
        result = '<a class="ow-wiki" href="mailto:example@example.com">mailto:example@example.com</a>'

        self.assertEqual(self.parser.toHtml(text), result)

    def testLinkAttachSimple(self):
        filename = "filename.tmp"
        text = "[[Attach:{}]]".format(filename)
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{filename}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachSimpleNotExists(self):
        filename = "filename_invalid.tmp"
        text = "[[Attach:{}]]".format(filename)
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{filename}</span>'.format(
            filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachSimpleDoubleQuotes(self):
        filename = "filename.tmp"
        text = '[[Attach:"{}"]]'.format(filename)
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{filename}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachSimpleDoubleQuotesNotExists(self):
        filename = "filename_invalid.tmp"
        text = '[[Attach:"{}"]]'.format(filename)
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{filename}</span>'.format(
            filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachSimpleSingleQuotes(self):
        filename = "filename.tmp"
        text = "[[Attach:'{}']]".format(filename)
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{filename}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachSimpleSingleQuotesNotExists(self):
        filename = "filename_invalid.tmp"
        text = "[[Attach:'{}']]".format(filename)
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{filename}</span>'.format(
            filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrow(self):
        filename = "filename.tmp"
        comment = "bla bla bla"
        text = "[[{comment} -> Attach:{filename}]]".format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrowNotExists(self):
        filename = "filename_invalid.tmp"
        comment = "bla bla bla"
        text = "[[{comment} -> Attach:{filename}]]".format(
            comment=comment, filename=filename
        )
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{comment}</span>'.format(
            comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrowDoubleQoutes(self):
        filename = "filename.tmp"
        comment = "bla bla bla"
        text = '[[{comment} -> Attach:"{filename}"]]'.format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrowDoubleQoutesNotExists(self):
        filename = "filename_invalid.tmp"
        comment = "bla bla bla"
        text = '[[{comment} -> Attach:"{filename}"]]'.format(
            comment=comment, filename=filename
        )
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{comment}</span>'.format(
            comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrowSingleQoutes(self):
        filename = "filename.tmp"
        comment = "bla bla bla"
        text = "[[{comment} -> Attach:'{filename}']]".format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentArrowSingleQoutesNotExists(self):
        filename = "filename_invalid.tmp"
        comment = "bla bla bla"
        text = "[[{comment} -> Attach:'{filename}']]".format(
            comment=comment, filename=filename
        )
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{comment}</span>'.format(
            comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachWithSpacesCommentArrowSingleQoutes(self):
        filename = "файл с пробелами.tmp"
        comment = "bla bla bla"
        text = "[[{comment} -> Attach:'{filename}']]".format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachWithSpacesCommentArrowDoubleQoutes(self):
        filename = "файл с пробелами.tmp"
        comment = "bla bla bla"
        text = '[[{comment} -> Attach:"{filename}"]]'.format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipe(self):
        filename = "filename.tmp"
        comment = "bla bla bla"
        text = "[[Attach:{filename} | {comment}]]".format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipeNotExists(self):
        filename = "filename_invalid.tmp"
        comment = "bla bla bla"
        text = "[[Attach:{filename} | {comment}]]".format(
            comment=comment, filename=filename
        )
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{comment}</span>'.format(
            comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipeDoubleQuotes(self):
        filename = "filename.tmp"
        comment = "bla bla bla"
        text = '[[Attach:"{filename}" | {comment}]]'.format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipeDoubleQuotesNotExists(self):
        filename = "filename_invalid.tmp"
        comment = "bla bla bla"
        text = '[[Attach:"{filename}" | {comment}]]'.format(
            comment=comment, filename=filename
        )
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{comment}</span>'.format(
            comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipeSingleQuotes(self):
        filename = "filename.tmp"
        comment = "bla bla bla"
        text = "[[Attach:'{filename}' | {comment}]]".format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachCommentPipeSingleQuotesNotExists(self):
        filename = "filename_invalid.tmp"
        comment = "bla bla bla"
        text = "[[Attach:'{filename}' | {comment}]]".format(
            comment=comment, filename=filename
        )
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{comment}</span>'.format(
            comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachWithSpacesCommentPipeSingleQuotes(self):
        filename = "файл с пробелами.tmp"
        comment = "bla bla bla"
        text = "[[Attach:'{filename}' | {comment}]]".format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachWithSpacesCommentPipeDoubleQuotes(self):
        filename = "файл с пробелами.tmp"
        comment = "bla bla bla"
        text = '[[Attach:"{filename}" | {comment}]]'.format(
            comment=comment, filename=filename
        )
        expected = '<a class="ow-wiki ow-link-attach ow-attach-file" href="{dir}/{filename}">{comment}</a>'.format(
            dir=PAGE_ATTACH_DIR, filename=filename, comment=comment
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageSimple(self):
        filename = "accept.png"
        text = "бла-бла-бла \n[[Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a class="ow-wiki ow-link-attach ow-attach-file" href="{attach_path}">{filename}</a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path, filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageSimpleNotExists(self):
        filename = "invalid.png"
        text = "бла-бла-бла \n[[Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        expected = 'бла-бла-бла \n<span class="ow-wiki ow-link-attach ow-attach-error">{filename}</span> бла-бла-бла\nбла-бла-бла'.format(
            filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageSimpleDoublleQuotes(self):
        filename = "accept.png"
        text = 'бла-бла-бла \n[[Attach:"{filename}"]] бла-бла-бла\nбла-бла-бла'.format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a class="ow-wiki ow-link-attach ow-attach-file" href="{attach_path}">{filename}</a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path, filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageSimpleSingleQuotes(self):
        filename = "accept.png"
        text = "бла-бла-бла \n[[Attach:'{filename}']] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected = 'бла-бла-бла \n<a class="ow-wiki ow-link-attach ow-attach-file" href="{attach_path}">{filename}</a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path, filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testLinkAttachImageArrow(self):
        filename = "accept.png"
        text = "бла-бла-бла \n[[Attach:{filename} -> Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected_regex = 'бла-бла-бла \n<a class="ow-wiki" href="{attach_path}"><img class="ow-image" src="{attach_path}\\?rnd=\\d+"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path
        )

        result = self.parser.toHtml(text)
        self.assertIsNotNone(re.match(expected_regex, result))

    def testLinkAttachImageArrowNotExists(self):
        filename = "invalid.png"
        text = "бла-бла-бла \n[[Attach:{filename} -> Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{filename}</span>'.format(
            filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertIn(expected, result)

    def testLinkAttachImageArrowSingleQuotes(self):
        filename = "accept.png"
        text = "бла-бла-бла \n[[Attach:'{filename}' -> Attach:'{filename}']] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected_regex = 'бла-бла-бла \n<a class="ow-wiki" href="{attach_path}"><img class="ow-image" src="{attach_path}\\?rnd=\\d+"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path
        )

        result = self.parser.toHtml(text)
        self.assertIsNotNone(re.match(expected_regex, result))

    def testLinkAttachImageArrowDoubleQuotes(self):
        filename = "accept.png"
        text = 'бла-бла-бла \n[[Attach:"{filename}" -> Attach:"{filename}"]] бла-бла-бла\nбла-бла-бла'.format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected_regex = 'бла-бла-бла \n<a class="ow-wiki" href="{attach_path}"><img class="ow-image" src="{attach_path}\\?rnd=\\d+"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path
        )

        result = self.parser.toHtml(text)
        self.assertIsNotNone(re.match(expected_regex, result))

    def testLinkAttachImagePipe(self):
        filename = "accept.png"
        text = "бла-бла-бла \n[[Attach:{filename} | Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected_regex = 'бла-бла-бла \n<a class="ow-wiki" href="{attach_path}"><img class="ow-image" src="{attach_path}\\?rnd=\\d+"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path
        )

        result = self.parser.toHtml(text)
        self.assertIsNotNone(re.match(expected_regex, result))

    def testLinkAttachImagePipeNotExists(self):
        filename = "invalid.png"
        text = "бла-бла-бла \n[[Attach:{filename} | Attach:{filename}]] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        expected = '<span class="ow-wiki ow-link-attach ow-attach-error">{filename}</span>'.format(
            filename=filename
        )

        result = self.parser.toHtml(text)
        self.assertIn(expected, result)

    def testLinkAttachImagePipeSingleQuotes(self):
        filename = "accept.png"
        text = "бла-бла-бла \n[[Attach:'{filename}' | Attach:'{filename}']] бла-бла-бла\nбла-бла-бла".format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected_regex = 'бла-бла-бла \n<a class="ow-wiki" href="{attach_path}"><img class="ow-image" src="{attach_path}\\?rnd=\\d+"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path
        )

        result = self.parser.toHtml(text)
        self.assertIsNotNone(re.match(expected_regex, result))

    def testLinkAttachImagePipeDoubleQuotes(self):
        filename = "accept.png"
        text = 'бла-бла-бла \n[[Attach:"{filename}" | Attach:"{filename}"]] бла-бла-бла\nбла-бла-бла'.format(
            filename=filename
        )
        attach_path = "{}/{}".format(PAGE_ATTACH_DIR, filename)
        expected_regex = 'бла-бла-бла \n<a class="ow-wiki" href="{attach_path}"><img class="ow-image" src="{attach_path}\\?rnd=\\d+"/></a> бла-бла-бла\nбла-бла-бла'.format(
            attach_path=attach_path
        )

        result = self.parser.toHtml(text)
        self.assertIsNotNone(re.match(expected_regex, result))

    def testPageProtocolLink(self):
        uid = self.testPage.getUid()
        text = f"бла-бла-бла [[page://{uid}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page" href="page://{uid}">{self.testPage.display_title}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkQuotes(self):
        uid = "пример-страницы"
        self.testPage.setUid(uid)
        text = f"бла-бла-бла [[page://{uid}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page" href="page://{quote(uid)}">{self.testPage.display_title}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkAnchor(self):
        uid = self.testPage.getUid()
        text = f"бла-бла-бла [[page://{uid}/#anchor]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page" href="page://{uid}/#anchor">{self.testPage.display_title}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkWithAnchorQuoted(self):
        uid = "пример-страницы"
        self.testPage.setUid(uid)
        text = f"бла-бла-бла [[page://{uid}/#anchor]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page" href="page://{quote(uid)}/#anchor">{self.testPage.display_title}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkInvalidUid(self):
        uid = "invalid_uid"
        text = f"бла-бла-бла [[page://{uid}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page ow-link-page-error" href="page://{uid}">page://{uid}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkInvalidUidQuotes(self):
        uid = "неправильный-uid"
        text = f"бла-бла-бла [[page://{uid}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page ow-link-page-error" href="page://{quote(uid)}">page://{uid}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkQuotesArrowComment(self):
        comment = "Комментарий к ссылке"
        uid = "пример-страницы"
        self.testPage.setUid(uid)
        text = f"бла-бла-бла [[{comment} -> page://{uid}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page" href="page://{quote(uid)}">{comment}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolInvalidLinkQuotesArrowComment(self):
        comment = "Комментарий к ссылке"
        uid = "неправильный-uid"
        text = f"бла-бла-бла [[{comment} -> page://{uid}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page ow-link-page-error" href="page://{quote(uid)}">{comment}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkWithAnchorQuotesArrowComment(self):
        comment = "Комментарий к ссылке"
        uid = "пример-страницы"
        self.testPage.setUid(uid)
        text = f"бла-бла-бла [[{comment} -> page://{uid}/#anchor]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page" href="page://{quote(uid)}/#anchor">{comment}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkQuotesPipeComment(self):
        comment = "Комментарий к ссылке"
        uid = "пример-страницы"
        self.testPage.setUid(uid)
        text = f"бла-бла-бла [[page://{uid} | {comment}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page" href="page://{quote(uid)}">{comment}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolInvalidLinkQuotesPipeComment(self):
        comment = "Комментарий к ссылке"
        uid = "неправильный-uid"
        text = f"бла-бла-бла [[page://{uid} | {comment}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page ow-link-page-error" href="page://{quote(uid)}">{comment}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testPageProtocolLinkWithAnchorQuotesPipeComment(self):
        comment = "Комментарий к ссылке"
        uid = "пример-страницы"
        self.testPage.setUid(uid)
        text = f"бла-бла-бла [[page://{uid}/#anchor | {comment}]] бла-бла-бла"
        expected = f'бла-бла-бла <a class="ow-wiki ow-link-page" href="page://{quote(uid)}/#anchor">{comment}</a> бла-бла-бла'

        result = self.parser.toHtml(text)
        self.assertEqual(result, expected)

    def testNonLatinURL(self):
        url = "https://пример.рф"
        text = f"бла-бла-бла \n[[{url}]] бла-бла-бла\nбла-бла-бла"
        expected = f'бла-бла-бла \n<a class="ow-wiki" href="{url}">{url}</a> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(self.parser.toHtml(text), expected)

    def testNonLatinURLArrowSpaces(self):
        url = "https://пример.рф"
        comment = "Комментарий"
        text = f"бла-бла-бла \n[[{comment} -> {url}]] бла-бла-бла\nбла-бла-бла"
        expected = f'бла-бла-бла \n<a class="ow-wiki" href="{url}">{comment}</a> бла-бла-бла\nбла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), expected)

    def testNonLatinURLArrowNoSpaces(self):
        url = "https://пример.рф"
        comment = "Комментарий"
        text = f"бла-бла-бла \n[[{comment}->{url}]] бла-бла-бла\nбла-бла-бла"
        expected = f'бла-бла-бла \n<a class="ow-wiki" href="{url}">{comment}</a> бла-бла-бла\nбла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), expected)

    def testNonLatinURLPipeSpaces(self):
        url = "https://пример.рф"
        comment = "Комментарий"
        text = f"бла-бла-бла \n[[{url} | {comment}]] бла-бла-бла\nбла-бла-бла"
        expected = f'бла-бла-бла \n<a class="ow-wiki" href="{url}">{comment}</a> бла-бла-бла\nбла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), expected)

    def testNonLatinURLPipeNoSpaces(self):
        url = "https://пример.рф"
        comment = "Комментарий"
        text = f"бла-бла-бла \n[[{url}|{comment}]] бла-бла-бла\nбла-бла-бла"
        expected = f'бла-бла-бла \n<a class="ow-wiki" href="{url}">{comment}</a> бла-бла-бла\nбла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), expected)

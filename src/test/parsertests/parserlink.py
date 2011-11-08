#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import cgi
import unittest
import hashlib

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application

from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserLinkTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "866"

        self.filesPath = u"../test/samplefiles/"

        self.url1 = u"http://example.com"
        self.url2 = u"http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"
        self.urlimage = u"http://example.com/image.png"

        self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
        self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

        self.__createWiki()
        
        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)
    

    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)
        WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 2"], u"#Страница3", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 2"], u"# Страница 4", [])
        self.testPage = self.rootwiki[u"Страница 2"]
        
        files = [u"accept.png", u"add.png", u"anchor.png", u"filename.tmp", 
                u"файл с пробелами.tmp", u"картинка с пробелами.png", 
                u"image.jpg", u"image.jpeg", u"image.png", u"image.tif", u"image.tiff", u"image.gif",
                u"image_01.JPG", u"dir", u"dir.xxx", u"dir.png"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)
    

    def tearDown(self):
        removeWiki (self.path)


    def testUrl1 (self):
        text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (self.url1)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testUrl2 (self):
        text = u"бла-бла-бла \ntest %s бла-бла-бла\nбла-бла-бла" % (self.url2)
        result = u'бла-бла-бла \ntest <A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, self.url2)

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testLink1 (self):
        text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (self.url1)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testLink2 (self):
        text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (self.url2)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, cgi.escape (self.url2) )

        self.assertEqual (self.parser.toHtml (text), result)


    def testLink3 (self):
        url = "http://jenyay.net/social/feed.png"

        text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (url)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (url, url)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLink4 (self):
        text = u"[[http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431 | Ссылко]]"
        result = u'<A HREF="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">Ссылко</A>'

        self.assertEqual (self.parser.toHtml (text), result)

    
    def testLink5 (self):
        text = u"[[Ссылко -> http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431]]"
        result = u'<A HREF="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">Ссылко</A>'

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testCommentLink1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testCommentLink2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testCommentLink3 (self):
        comment = u"Ссылко с '''полужирным''' текстом"
        text = u"бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, u"Ссылко с <B>полужирным</B> текстом")

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testCommentLink4 (self):
        comment = u"Ссылко с '''полужирным''' текстом"
        text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, u"Ссылко с <B>полужирным</B> текстом")

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testCommentLink5 (self):
        text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (self.url1, self.url1)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

        self.assertEqual (self.parser.toHtml (text), result)


    def testCommentLink6 (self):
        text = u"бла-бла-бла \n[[Комментарий с <, > и & -> %s]] бла-бла-бла\nбла-бла-бла" % (self.url1)
        result = u'бла-бла-бла \n<A HREF="%s">Комментарий с &lt;, &gt; и &amp;</A> бла-бла-бла\nбла-бла-бла' % (self.url1)

        self.assertEqual (self.parser.toHtml (text), result)


    def testCommentLink7 (self):
        text = u"бла-бла-бла \n[[%s | Комментарий с <, > и &]] бла-бла-бла\nбла-бла-бла" % (self.url1)
        result = u'бла-бла-бла \n<A HREF="%s">Комментарий с &lt;, &gt; и &amp;</A> бла-бла-бла\nбла-бла-бла' % (self.url1)

        self.assertEqual (self.parser.toHtml (text), result)


    def testStrikeLink1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[{-%s-} -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><STRIKE>%s</STRIKE></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testStrikeLink2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | {-%s-}]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><STRIKE>%s</STRIKE></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testPageLinks (self):
        for link in self.pagelinks:
            text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (link)
            result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (link, link)

            self.assertEqual (self.parser.toHtml (text), result)


    def testPageLinkSharp1 (self):
        """
        Проверка ссылок на страницы с #
        """
        text = u"бла-бла-бла \n[[#Страница3]] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<A HREF="#Страница3">#Страница3</A> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result)


    def testPageLinkSharp2 (self):
        """
        Проверка ссылок на страницы с #
        """
        text = u"бла-бла-бла \n[[# Страница 4]] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<A HREF="# Страница 4"># Страница 4</A> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result)


    def testAnchor1 (self):
        """
        Проверка создания якорей
        """
        text = u"бла-бла-бла \n[[#anchor]] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<A NAME="anchor"></A> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result)


    def testAnchor2 (self):
        """
        Проверка создания якорей
        """
        text = u"бла-бла-бла \n[[#якорь]] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<A NAME="якорь"></A> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result)


    def testNoFormatLinks1 (self):
        for link in self.pagelinks:
            text = u"бла-бла-бла \n[[%s | [='''ля-ля-ля'''=] ]] бла-бла-бла\nбла-бла-бла" % (link)
            result = u"бла-бла-бла \n<A HREF=\"%s\">'''ля-ля-ля'''</A> бла-бла-бла\nбла-бла-бла" % (link)

            self.assertEqual (self.parser.toHtml (text), result)


    def testNoFormatLinks2 (self):
        for link in self.pagelinks:
            text = u"бла-бла-бла \n[[[='''ля-ля-ля'''=] -> %s]] бла-бла-бла\nбла-бла-бла" % (link)
            result = u"бла-бла-бла \n<A HREF=\"%s\">'''ля-ля-ля'''</A> бла-бла-бла\nбла-бла-бла" % (link)

            self.assertEqual (self.parser.toHtml (text), result)


    def testTexLinks1 (self):
        for link in self.pagelinks:
            text = u"бла-бла-бла \n[[%s | {$e^x$} ]] бла-бла-бла\nбла-бла-бла" % (link)
            result_begin = u'бла-бла-бла \n<A HREF="%s"><IMG SRC="__attach/__thumb/eqn_' % (link)

            self.assertTrue (self.parser.toHtml (text).startswith (result_begin) )


    def testTexLinks2 (self):
        for link in self.pagelinks:
            text = u"бла-бла-бла \n[[{$e^x$} -> %s]] бла-бла-бла\nбла-бла-бла" % (link)
            result_begin = u'бла-бла-бла \n<A HREF="%s"><IMG SRC="__attach/__thumb/eqn_' % (link)

            self.assertTrue (self.parser.toHtml (text).startswith (result_begin) )
    

    def testPageCommentsLinks1 (self):
        for n in range ( len (self.pagelinks)):
            link = self.pagelinks[n]
            comment = self.pageComments[n]

            text = u"бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (link, comment)
            result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (link, comment)

            self.assertEqual (self.parser.toHtml (text), result)
    

    def testPageCommentsLinks2 (self):
        for n in range ( len (self.pagelinks)):
            link = self.pagelinks[n]
            comment = self.pageComments[n]

            text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, link)
            result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (link, comment)

            self.assertEqual (self.parser.toHtml (text), result)


    def testLinkSubscript1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | '_%s_']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><SUB>%s</SUB></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkSubscript2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[['_%s_' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><SUB>%s</SUB></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkSuperscript1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | '^%s^']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><SUP>%s</SUP></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkSuperscript2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[['^%s^' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><SUP>%s</SUP></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkBoldItalic1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | ''''%s'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><B><I>%s</I></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkBoldItalic2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[''''%s'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><B><I>%s</I></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkBold1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | '''%s''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><B>%s</B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkBold2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[['''%s''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><B>%s</B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkItalic1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | ''%s'']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><I>%s</I></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkItalic2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[''%s'' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><I>%s</I></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testUrlImage1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (self.urlimage)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.urlimage, self.urlimage)

        self.assertEqual (self.parser.toHtml (text), result)


    def testUrlImage2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.urlimage)
        result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.urlimage, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testUrlImage3 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (self.urlimage, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><IMG SRC="%s"/></A> бла-бла-бла\nбла-бла-бла' % (self.url2, self.urlimage)

        self.assertEqual (self.parser.toHtml (text), result)


    def testUrlImage4 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (self.url2, self.urlimage)
        result = u'бла-бла-бла \n<A HREF="%s"><IMG SRC="%s"/></A> бла-бла-бла\nбла-бла-бла' % (self.url2, self.urlimage)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkUnderline1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | {+%s+}]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><U>%s</U></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testLinkUnderline2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[{+%s+} -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><U>%s</U></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc1 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | ''''_%s_'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><B><SUB>%s</SUB></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc2 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[ ''''_%s_'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><B><SUB>%s</SUB></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc3 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | ''''^%s^'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><B><SUP>%s</SUP></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc4 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[ ''''^%s^'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><B><SUP>%s</SUP></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc5 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | '''_%s_''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><I><SUB>%s</SUB></I></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc6 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[ '''_%s_''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><I><SUB>%s</SUB></I></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc7 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | '''^%s^''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><I><SUP>%s</SUP></I></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc8 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[ '''^%s^''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><I><SUP>%s</SUP></I></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc9 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | ''''%s'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><B><I>%s</I></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc10 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[ ''''%s'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><B><I>%s</I></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc11 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[%s | ''''%s'''']] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
        result = u'бла-бла-бла \n<A HREF="%s"><B><I>%s</I></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)


    def testAdHoc12 (self):
        comment = u"Ссылко"
        text = u"бла-бла-бла \n[[ ''''%s'''' -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
        result = u'бла-бла-бла \n<A HREF="%s"><B><I>%s</I></B></A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

        self.assertEqual (self.parser.toHtml (text), result)



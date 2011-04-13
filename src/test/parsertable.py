#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from utils import removeWiki

from core.tree import WikiDocument
from core.attachment import Attachment
from core.application import Application

from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parserfactory import ParserFactory


class ParserTableTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "utf8"
		self.filesPath = u"../test/samplefiles/"

		self.__createWiki()
		
		factory = ParserFactory()
		self.parser = factory.make (self.testPage, Application.config)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)
		WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
		self.testPage = self.rootwiki[u"Страница 2"]
		

	def tearDown(self):
		removeWiki (self.path)
	

	def testTable1 (self):
		text = u"""бла-бла-бла
|| border=1
|| Ячейка 1 ||Ячейка 2 || Ячейка 3||
||Ячейка 4||Ячейка 5||Ячейка 6||
"""
		
		result = u'''бла-бла-бла
<TABLE border=1><TR><TD ALIGN="CENTER">Ячейка 1</TD><TD ALIGN="LEFT">Ячейка 2</TD><TD ALIGN="RIGHT">Ячейка 3</TD></TR><TR><TD>Ячейка 4</TD><TD>Ячейка 5</TD><TD>Ячейка 6</TD></TR></TABLE>'''
	
		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testTable2 (self):
		text = u"""|| border=1
|| '''Синтаксис''' || '''Результат''' || '''Комментарий''' ||
||[@http://example.com@]||http://example.com||Ссылка на адрес в интернете||
||[@[[http://example.com]]@]||[[http://example.com]]||Ссылка на адрес в интернете||
||[@[[Пример ссылки -> http://example.com]]@]||[[Пример ссылки -> http://example.com]]||Ссылка на адрес в интернете с заданным текстом||
||[@[[http://example.com | Пример ссылки]]@]||[[http://example.com | Пример ссылки]]||Ссылка на адрес в интернете с заданным текстом||
"""
		
		result = u'''<TABLE border=1><TR><TD ALIGN="CENTER"><B>Синтаксис</B></TD><TD ALIGN="CENTER"><B>Результат</B></TD><TD ALIGN="CENTER"><B>Комментарий</B></TD></TR><TR><TD><PRE>http://example.com</PRE></TD><TD><A HREF="http://example.com">http://example.com</A></TD><TD>Ссылка на адрес в интернете</TD></TR><TR><TD><PRE>[[http://example.com]]</PRE></TD><TD><A HREF="http://example.com">http://example.com</A></TD><TD>Ссылка на адрес в интернете</TD></TR><TR><TD><PRE>[[Пример ссылки -&gt; http://example.com]]</PRE></TD><TD><A HREF="http://example.com">Пример ссылки</A></TD><TD>Ссылка на адрес в интернете с заданным текстом</TD></TR><TR><TD><PRE>[[http://example.com | Пример ссылки]]</PRE></TD><TD><A HREF="http://example.com">Пример ссылки</A></TD><TD>Ссылка на адрес в интернете с заданным текстом</TD></TR></TABLE>'''
	
		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testTable3 (self):
		text = u"""||border=1 width=350
||left aligned \\
sdfsdf || centered || right aligned||
||left aligned [[<<]] dsfsdf || centered || right aligned||
||left aligned [[&lt;&lt;]] dsfsdf || centered || right aligned||
||left aligned [[<<]][[<<]] sdfsdfsdf || centered || right aligned||
"""
		
		result = u'''<TABLE border=1 width=350><TR><TD ALIGN="LEFT">left aligned sdfsdf</TD><TD ALIGN="CENTER">centered</TD><TD ALIGN="RIGHT">right aligned</TD></TR><TR><TD ALIGN="LEFT">left aligned <BR> dsfsdf</TD><TD ALIGN="CENTER">centered</TD><TD ALIGN="RIGHT">right aligned</TD></TR><TR><TD ALIGN="LEFT">left aligned <BR> dsfsdf</TD><TD ALIGN="CENTER">centered</TD><TD ALIGN="RIGHT">right aligned</TD></TR><TR><TD ALIGN="LEFT">left aligned <BR><BR> sdfsdfsdf</TD><TD ALIGN="CENTER">centered</TD><TD ALIGN="RIGHT">right aligned</TD></TR></TABLE>'''
	
		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


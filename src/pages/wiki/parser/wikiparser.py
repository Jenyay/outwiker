#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import os

from libs.pyparsing import Regex, Literal, replaceWith, LineStart, LineEnd, OneOrMore, Optional
from core.tree import RootWikiPage

from tokenfonts import FontsFactory
from tokennoformat import NoFormatFactory
from tokenpreformat import PreFormatFactory
from tokenthumbnail import ThumbnailFactory
from tokenheading import HeadingFactory
from tokenadhoc import AdHocFactory
from tokenhorline import HorLineFactory
from tokenlink import LinkFactory
from tokenalign import CenterAlignFactory, RightAlignFactory
from tokentable import TableFactory
from tokenurl import UrlFactory
from tokenurlimage import UrlImageFactory
from tokenattach import NotImageAttachFactory, ImageAttachFactory

from listparser import ListParser
from utils import noConvert, replaceBreakes, concatenate, convertToHTML, isImage



class ListParams (object):
	"""
	Параметры списков в парсере
	"""
	def __init__ (self, symbol, startTag, endTag):
		self.symbol = symbol
		self.startTag = startTag
		self.endTag = endTag



class Parser (object):
	def __init__ (self, page, maxSizeThumb = 250):
		self.page = page
		self.maxSizeThumb = maxSizeThumb

		self.unorderList = "*"
		self.orderList = "#"

		self.__createFontTokens()

		self.headings = HeadingFactory.make(self)
		self.thumb = ThumbnailFactory.make(self)
		self.noformat = NoFormatFactory.make(self)
		self.preformat = PreFormatFactory.make (self)
		self.horline = HorLineFactory.make(self)
		self.link = LinkFactory.make (self)
		self.centerAlign = CenterAlignFactory.make(self)
		self.rightAlign = RightAlignFactory.make (self)
		self.table = TableFactory.make(self)
		self.url = UrlFactory.make (self)
		self.urlImage = UrlImageFactory.make (self)
		self.attachesNotImage = NotImageAttachFactory.make (self)
		self.attachesImage = ImageAttachFactory.make (self)
		self.adhoctokens = AdHocFactory.make(self)

		self.listItemMarkup = (self.link |
				self.boldItalicized |
				self.bolded |
				self.italicized |
				self.code |
				self.preformat |
				self.noformat |
				self.urlImage |
				self.url |
				self.thumb |
				self.underlined |
				self.subscript |
				self.superscript |
				self.attachesImage |
				self.attachesNotImage
				)

		self.list = self.__getListToken ()

		self.wikiMarkup = (self.link |
				self.adhoctokens |
				self.subscript |
				self.superscript |
				self.boldItalicized |
				self.bolded |
				self.italicized |
				self.code |
				self.preformat |
				self.noformat |
				self.urlImage |
				self.url |
				self.thumb |
				self.underlined |
				self.horline |
				self.centerAlign |
				self.rightAlign |
				self.list |
				self.table |
				self.attachesImage |
				self.attachesNotImage |
				self.headings
				)


		# Нотация для ссылок
		self.linkMarkup = (self.adhoctokens |
				self.subscript |
				self.superscript |
				self.boldItalicized |
				self.bolded |
				self.italicized |
				self.urlImage |
				self.underlined |
				self.attachesImage
				)


	def __getListToken (self):
		allListsParams = [ListParams (self.unorderList, u"<UL>", u"</UL>"), ListParams (self.orderList, u"<OL>", u"</OL>")]
		self.listParser = ListParser (allListsParams, self.listItemMarkup)
		return self.listParser.getListToken()


	def __createFontTokens (self):
		self.italicized = FontsFactory.makeItalic (self)
		self.bolded = FontsFactory.makeBold (self)
		self.boldItalicized = FontsFactory.makeBoldItalic (self)
		self.underlined = FontsFactory.makeUnderline (self)
		self.subscript = FontsFactory.makeSubscript (self)
		self.superscript = FontsFactory.makeSuperscript (self)
		self.code = FontsFactory.makeCode (self)
	

	def toHtml (self, text):
		"""
		Сгенерить HTML без заголовков тима <HTML> и т.п.
		"""
		text = text.replace ("\\\n", "")
		return self.wikiMarkup.transformString(text)


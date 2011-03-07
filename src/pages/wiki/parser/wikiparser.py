#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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
from tokenlist import ListFactory


class Parser (object):
	def __init__ (self, page, config):
		self.page = page
		self.config = config

		self.italicized = FontsFactory.makeItalic (self)
		self.bolded = FontsFactory.makeBold (self)
		self.boldItalicized = FontsFactory.makeBoldItalic (self)
		self.underlined = FontsFactory.makeUnderline (self)
		self.subscript = FontsFactory.makeSubscript (self)
		self.superscript = FontsFactory.makeSuperscript (self)
		self.code = FontsFactory.makeCode (self)
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
		self.lists = ListFactory.make (self)

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
				self.lists |
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


	def toHtml (self, text):
		"""
		Сгенерить HTML без заголовков типа <HTML> и т.п.
		"""
		text = text.replace ("\\\n", "")
		return self.parseWikiMarkup(text)


	def parseWikiMarkup (self, text):
		return self.wikiMarkup.transformString (text)


	def parseListItemMarkup (self, text):
		return self.listItemMarkup.transformString (text)


	def parseLinkMarkup (self, text):
		return self.linkMarkup.transformString (text)


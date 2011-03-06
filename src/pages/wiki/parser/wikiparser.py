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

		self.attachString = u"Attach:"
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

		self.table = self.__getTableToken ()
		self.url = self.__getUrlToken ()
		self.urlImage = self.__getUrlImageToken ()
		self.attachesNotImage = self.__getNotImageAttachTokens ()
		self.attachesImage = self.__getImageAttachTokens ()
		
		self.list = self.__getListToken ()

		self.adhoctokens = AdHocFactory.make(self)


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



	def __getUrlToken (self):
		token =  Regex ("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)\\.)[-A-Za-z0-9\\.]+[-A-Za-z0-9]+)(:[0-9]*)?(/([-A-Za-z0-9_,\\$\\.\\+\\!\\*\\(\\):@&=\\?/~\\#\\%]*[-A-Za-z0-9_\\$\\+\\!\\*\\(\\):@&=\\?/~\\#\\%])?)?", re.IGNORECASE)

		token.setParseAction(self.__convertToUrlLink)
		return token


	def __getUrlImageToken (self):
		token = Regex ("(https?|ftp)://[a-z0-9-]+(\.[a-z0-9-]+)+(/[-._\w%]+)*/[-\w_.%]+\.(gif|png|jpe?g|bmp|tiff?)", re.IGNORECASE)
		token.setParseAction(self.__convertToImage)
		return token


	def __getListToken (self):
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

		allListsParams = [ListParams (self.unorderList, u"<UL>", u"</UL>"), ListParams (self.orderList, u"<OL>", u"</OL>")]

		self.listParser = ListParser (allListsParams, self.listItemMarkup)

		return self.listParser.getListToken()


	def __getTableToken (self):
		tableCell = Regex ("(?P<text>.*?)\\|\\|")
		tableCell.setParseAction(self.__convertTableCell)

		tableRow = LineStart() + "||" + OneOrMore (tableCell) + Optional (LineEnd())
		tableRow.setParseAction(self.__convertTableRow)

		table = LineStart() + Regex ("\\|\\| *(?P<params>.+)?") + LineEnd() + OneOrMore (tableRow)
		table.setParseAction(self.__convertTable)

		return table


	def __convertTableCell (self, s, loc, toks):
		text = toks["text"]

		leftAlign = toks["text"][-1] in " \t"
		
		# Условие в скобках связано с тем, что первый пробел попадает 
		# или не попадает в токен в зависимости от того, первая ячейка в строке или первая ячейка в строке или нет
		rightAlign = loc > 0 and (s[loc - 1] in " \t" or s[loc] in " \t")

		align = u''

		if leftAlign and rightAlign:
			align = u' ALIGN="CENTER"'
		elif leftAlign:
			align = u' ALIGN="LEFT"'
		elif rightAlign:
			align = u' ALIGN="RIGHT"'

		result = u'<TD%s>%s</TD>' % (align, self.wikiMarkup.transformString (replaceBreakes (text.strip() ) ) )

		return result


	def __convertTableRow (self, s, l, t):
		if t[-1] == "\n":
			lastindex = len (t) - 1
		else:
			lastindex = len (t)

		result = u"<TR>"
		for n in range (1, lastindex):
			result += t[n]

		result += "</TR>"

		return result


	def __convertTable (self, s, l, t):
		result = u"<TABLE %s>" % t[0][2:].strip()
		for n in range (2, len (t)):
			result += t[n]

		result += "</TABLE>"

		return result
	

	def __createFontTokens (self):
		self.italicized = FontsFactory.makeItalic (self)
		self.bolded = FontsFactory.makeBold (self)
		self.boldItalicized = FontsFactory.makeBoldItalic (self)
		self.underlined = FontsFactory.makeUnderline (self)
		self.subscript = FontsFactory.makeSubscript (self)
		self.superscript = FontsFactory.makeSuperscript (self)
		self.code = FontsFactory.makeCode (self)
	

	def __convertToImage (self, s, l, t):
		return u'<IMG SRC="%s">' % t[0]


	def sortByLength (self, fname1, fname2):
		"""
		Функция для сортировки имен по длине имени
		"""
		if len (fname1) > len (fname2):
			return 1
		elif len (fname1) < len (fname2):
			return -1

		return 0


	def __getImageAttachTokens (self):
		"""
		Создать элементы из прикрепленных файлов.
		Отдельно картинки, отдельно все файлы
		"""
		attachesImages = []

		attaches = self.page.attachment
		attaches.sort (self.sortByLength, reverse=True)

		for attach in attaches:
			if isImage (attach):
				fname = os.path.basename (attach)
				attach_token = self.attachString + Literal (fname)
				attach_token.setParseAction (replaceWith (self.__getReplaceForImageAttach (fname) ) )
				attachesImages.append (attach_token)

		return concatenate (attachesImages)

	
	def __getNotImageAttachTokens (self):
		"""
		Создать элементы из прикрепленных файлов.
		Отдельно картинки, отдельно все файлы
		"""
		attachesAll = []

		attaches = self.page.attachment
		attaches.sort (self.sortByLength, reverse=True)

		for attach in attaches:
			if not isImage (attach):
				fname = os.path.basename (attach)
				attach = self.attachString + Literal (fname)
				attach.setParseAction (replaceWith (self.__getReplaceForAttach (fname) ) )
				attachesAll.append (attach)

		return concatenate (attachesAll)


	def __getUrlTag (self, url, comment):
		return '<A HREF="%s">%s</A>' % (url.strip(), self.linkMarkup.transformString (comment.strip()) )


	def __convertToUrlLink (self, s, l, t):
		"""
		Преобразовать ссылку на инетрнет-адрес
		"""
		if (not t[0].startswith ("http://") and
				not t[0].startswith ("ftp://") and
				not t[0].startswith ("news://") and
				not t[0].startswith ("gopher://") and
				not t[0].startswith ("telnet://") and
				not t[0].startswith ("nttp://") and
				not t[0].startswith ("file://") and
				not t[0].startswith ("https://")
				):
			return self.__getUrlTag ("http://" + t[0], t[0])

		return self.__getUrlTag (t[0], t[0])


	def __getReplaceForAttach (self, fname):
		"""
		Получить строку для замены ссылкой на прикрепленный файл
		"""
		return '<A HREF="%s/%s">%s</A>' % (RootWikiPage.attachDir, fname, fname)


	def __getReplaceForImageAttach (self, fname):
		"""
		Получить строку для замены ссылкой на прикрепленный файл
		"""
		return '<IMG SRC="%s/%s">' % (RootWikiPage.attachDir, fname)


	def toHtml (self, text):
		"""
		Сгенерить HTML без заголовков тима <HTML> и т.п.
		"""
		text = text.replace ("\\\n", "")
		return self.wikiMarkup.transformString(text)


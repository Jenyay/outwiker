#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import os

from libs.pyparsing import QuotedString, Regex, Empty, Literal, replaceWith, LineStart, LineEnd, OneOrMore, ZeroOrMore, NotAny, Or, Optional, StringEnd
from core.tree import RootWikiPage

from pages.wiki.parser.tokenthumbnail import ThumbnailFactory
from pages.wiki.parser.listparser import ListParser
from pages.wiki.parser.utils import noConvert, replaceBreakes



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

		self.__attachString = u"Attach:"
		self.heading1_Regex = "^!!\s+(?P<title>.*)$"
		self.heading2_Regex = "^!!!\s+(?P<title>.*)$"
		self.heading3_Regex = "^!!!!\s+(?P<title>.*)$"
		self.heading4_Regex = "^!!!!!\s+(?P<title>.*)$"
		self.heading5_Regex = "^!!!!!!\s+(?P<title>.*)$"
		self.heading6_Regex = "^!!!!!!!\s+(?P<title>.*)$"
		self.codeStart = "@@"
		self.codeEnd = "@@"
		self.superscriptStart = "'^"
		self.superscriptEnd = "^'"
		self.subscriptStart = "'_"
		self.subscriptEnd = "_'"
		self.underlineStart = "{+"
		self.underlineEnd = "+}"
		self.boldItalicStart = "''''"
		self.boldItalicEnd = "''''"
		self.boldStart = "'''"
		self.boldEnd = "'''"
		self.italicStart = "''"
		self.italicEnd = "''"
		self.unorderList = "*"
		self.orderList = "#"
		self.rightRegex = "% *?right *?%(?P<text>.*?)(?P<end>(\n\n)|\Z)"
		self.centerRegex = "% *?center *?%(?P<text>.*?)(?P<end>(\n\n)|\Z)"
		self.linkStart = "[["
		self.linkEnd = "]]"
		self.preFormatStart = "[@"
		self.preFormatEnd = "@]"
		self.noFormatStart = "[="
		self.noFormatEnd = "=]"
		self.horLineRegEx = "----+"

		self.__createFontTokens()
		self.__createAdHocTokens()

		# Заголовки
		self.headings = self.__getHeadingTokens()

		self.noformat = self.__getNoFormatToken()
		self.preformat = self.__getPreformatToken()
		self.horline = self.__getHorLineToken()
		self.link = self.__getLinkToken()
		self.centerAlign = self.__getCenterAlignToken ()
		self.rightAlign = self.__getRightrAlignToken ()
		self.thumb = ThumbnailFactory.make(self)
		self.table = self.__getTableToken ()
		self.url = self.__getUrlToken ()
		self.urlImage = self.__getUrlImageToken ()
		self.attachesNotImage = self.__getNotImageAttachTokens ()
		self.attachesImage = self.__getImageAttachTokens ()
		
		self.list = self.__getListToken ()


		self.wikiMarkup = self.link | \
				self.boldItalicSubscripted | \
				self.boldItalicSuperscripted | \
				self.boldSubscripted | \
				self.boldSuperscripted | \
				self.italicSubscripted | \
				self.italicSuperscripted | \
				self.subscript | \
				self.superscript | \
				self.boldItalicized | \
				self.bolded | \
				self.italicized | \
				self.code |\
				self.preformat | \
				self.noformat | \
				self.urlImage | \
				self.url | \
				self.thumb | \
				self.underlined | \
				self.horline | \
				self.centerAlign | \
				self.rightAlign | \
				self.list | \
				self.table


		# Нотация для ссылок
		self.linkMarkup = self.boldItalicSubscripted | \
				self.boldItalicSuperscripted | \
				self.boldSubscripted | \
				self.boldSuperscripted | \
				self.italicSubscripted | \
				self.italicSuperscripted | \
				self.subscript | \
				self.superscript | \
				self.boldItalicized | \
				self.bolded | \
				self.italicized | \
				self.urlImage | \
				self.underlined

		self.__addTokens (self.attachesImage, self.wikiMarkup)
		self.__addTokens (self.attachesImage, self.listItemMarkup)
		self.__addTokens (self.attachesImage, self.linkMarkup)
		self.__addTokens (self.attachesNotImage, self.wikiMarkup)
		self.__addTokens (self.attachesNotImage, self.listItemMarkup)
		self.__addTokens (self.headings, self.wikiMarkup)

	
	def __getHorLineToken (self):
		return Regex(self.horLineRegEx).setParseAction (self.__convertToText ("<HR>"))
	

	def __getNoFormatToken (self):
		return QuotedString(self.noFormatStart, endQuoteChar = self.noFormatEnd, multiline = True).setParseAction(noConvert)
	

	def __getPreformatToken (self):
		return QuotedString(self.preFormatStart, endQuoteChar = self.preFormatEnd, multiline = True).setParseAction(self.__convertPreformat)


	def __getLinkToken (self):
		return QuotedString(self.linkStart, endQuoteChar = self.linkEnd, multiline = True).setParseAction(self.__convertToLink)
	

	def __getCenterAlignToken (self):
		return Regex (self.centerRegex, re.MULTILINE | re.DOTALL | re.IGNORECASE).setParseAction(self.__align ("CENTER") )


	def __getRightrAlignToken (self):
		return Regex(self.rightRegex, re.MULTILINE | re.DOTALL | re.IGNORECASE).setParseAction(self.__align ("RIGHT") )
	

	def __getUrlToken (self):
		token =  Regex ("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)\\.)[-A-Za-z0-9\\.]+[-A-Za-z0-9]+)(:[0-9]*)?(/([-A-Za-z0-9_,\\$\\.\\+\\!\\*\\(\\):@&=\\?/~\\#\\%]*[-A-Za-z0-9_\\$\\+\\!\\*\\(\\):@&=\\?/~\\#\\%])?)?", re.IGNORECASE)

		token.setParseAction(self.__convertToUrlLink)
		return token


	def __getUrlImageToken (self):
		token = Regex ("(https?|ftp)://[a-z0-9-]+(\.[a-z0-9-]+)+(/[-._\w%]+)*/[-\w_.%]+\.(gif|png|jpe?g|bmp|tiff?)", re.IGNORECASE)
		token.setParseAction(self.__convertToImage)
		return token


	def __getListToken (self):
		self.listItemMarkup = self.link | \
				self.boldItalicized | \
				self.bolded | \
				self.italicized | \
				self.code |\
				self.preformat | \
				self.noformat | \
				self.urlImage | \
				self.url | \
				self.thumb | \
				self.underlined | \
				self.subscript | \
				self.superscript 

		allListsParams = [ListParams (self.unorderList, u"<UL>", u"</UL>"), ListParams (self.orderList, u"<OL>", u"</OL>")]

		self.listParser = ListParser (allListsParams, self.listItemMarkup)

		return self.listParser.getListToken()


	def __addTokens (self, tokenList, srcToken):
		"""
		Добавить токены из списка tokenList к srcToken
		"""
		for token in tokenList:
			srcToken |= token


	def __getTableToken (self):
		tableCell = Regex ("(?P<text>.*?)\\|\\|")
		tableCell.setParseAction(self.__convertTableCell)

		tableRow = LineStart() + "||" + OneOrMore (tableCell) + Optional (LineEnd())
		tableRow.setParseAction(self.__convertTableRow)

		#table = LineStart() + Literal ("||") + Optional (Regex (".*")) + LineEnd() + OneOrMore (tableRow)
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
		self.italicized = QuotedString (self.italicStart, 
				endQuoteChar = self.italicEnd, 
				multiline = True).setParseAction(self.__convertToHTML("<I>","</I>"))

		self.bolded = QuotedString (self.boldStart, 
				endQuoteChar = self.boldEnd, 
				multiline = True).setParseAction(self.__convertToHTML("<B>","</B>"))

		self.boldItalicized = QuotedString (self.boldItalicStart, 
				endQuoteChar = self.boldItalicEnd, 
				multiline = True).setParseAction(self.__convertToHTML("<B><I>","</I></B>"))

		self.underlined = QuotedString (self.underlineStart, 
				endQuoteChar = self.underlineEnd, 
				multiline = True).setParseAction(self.__convertToHTML("<U>","</U>"))

		self.subscript = QuotedString (self.subscriptStart, 
				endQuoteChar = self.subscriptEnd, 
				multiline = True).setParseAction(self.__convertToHTML("<SUB>","</SUB>"))

		self.superscript = QuotedString (self.superscriptStart, 
				endQuoteChar = self.superscriptEnd, 
				multiline = True).setParseAction(self.__convertToHTML("<SUP>","</SUP>"))

		self.code = QuotedString (self.codeStart, 
				endQuoteChar = self.codeEnd, 
				multiline = True).setParseAction(self.__convertToHTML("<CODE>","</CODE>"))
	

	def __createAdHocTokens (self):
		"""
		Создать токены на отдельные случаи, с которыми возникают проблемы в общем случае
		"""
		self.boldSubscripted = QuotedString (self.boldStart, 
				endQuoteChar = self.subscriptEnd + self.boldEnd, 
				multiline = True).setParseAction(self.__convertToHtmlAdHoc("<B>", 
					"</B>",
					suffix = self.subscriptEnd))


		self.boldSuperscripted = QuotedString (self.boldStart, 
				endQuoteChar = self.superscriptEnd + self.boldEnd, 
				multiline = True).setParseAction(self.__convertToHtmlAdHoc("<B>", 
					"</B>",
					suffix = self.superscriptEnd))

		self.italicSubscripted = QuotedString (self.italicStart, 
				endQuoteChar = self.subscriptEnd + self.italicEnd, 
				multiline = True).setParseAction(self.__convertToHtmlAdHoc("<I>", 
					"</I>",
					suffix = self.subscriptEnd))


		self.italicSuperscripted = QuotedString (self.italicStart, 
				endQuoteChar = self.superscriptEnd + self.italicEnd, 
				multiline = True).setParseAction(self.__convertToHtmlAdHoc("<I>", 
					"</I>",
					suffix = self.superscriptEnd))

		self.boldItalicSubscripted = QuotedString (self.boldItalicStart, 
				endQuoteChar = self.subscriptEnd + self.boldItalicEnd, 
				multiline = True).setParseAction(self.__convertToHtmlAdHoc("<B><I>", 
					"</I></B>",
					suffix = self.subscriptEnd))

		self.boldItalicSuperscripted = QuotedString (self.boldItalicStart, 
				endQuoteChar = self.superscriptEnd + self.boldItalicEnd, 
				multiline = True).setParseAction(self.__convertToHtmlAdHoc("<B><I>", 
					"</I></B>",
					suffix = self.superscriptEnd))


	def __align (self, align):
		def __divTransform (s, l, t):
			return u'<DIV ALIGN="' + align + '">' + self.wikiMarkup.transformString (t["text"]) + '</DIV>' + t["end"]

		return __divTransform

	
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
			if self.__isImage (attach):
				fname = os.path.basename (attach)
				attach_token = self.__attachString + Literal (fname)
				attach_token.setParseAction (replaceWith (self.__getReplaceForImageAttach (fname) ) )
				attachesImages.append (attach_token)

		return attachesImages

	
	def __getNotImageAttachTokens (self):
		"""
		Создать элементы из прикрепленных файлов.
		Отдельно картинки, отдельно все файлы
		"""
		attachesAll = []

		attaches = self.page.attachment
		attaches.sort (self.sortByLength, reverse=True)

		for attach in attaches:
			if not self.__isImage (attach):
				fname = os.path.basename (attach)
				attach = self.__attachString + Literal (fname)
				attach.setParseAction (replaceWith (self.__getReplaceForAttach (fname) ) )
				attachesAll.append (attach)

		return attachesAll


	def __getHeadingTokens (self):
		"""
		Токены для заголовков H1 - H6
		"""
		tokens = []
		tokens.append (Regex (self.heading1_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H1>","</H1>") ) )
		tokens.append (Regex (self.heading2_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H2>","</H2>") ) )
		tokens.append (Regex (self.heading3_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H3>","</H3>") ) )
		tokens.append (Regex (self.heading4_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H4>","</H4>") ) )
		tokens.append (Regex (self.heading5_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H5>","</H5>") ) )
		tokens.append (Regex (self.heading6_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H6>","</H6>") ) )

		return tokens


	def __isImage (self, fname):
		images_ext = [".png", ".bmp", ".gif", ".tif", ".tiff", ".jpg", ".jpeg"]

		for ext in images_ext:
			if fname.lower().endswith (ext):
				return True

		return False
		

	def __convertToHTML (self, opening, closing):
		def conversionParseAction(s,l,t):
			return opening + self.wikiMarkup.transformString (t[0]) + closing
		return conversionParseAction


	def __convertToHtmlAdHoc(self, opening, closing, prefix=u"", suffix=u""):
		"""
		Преобразование в HTML для отдельный случаев, когда надо добавить в начало или конец обрабатываемой строки префикс или суффикс
		"""
		def conversionParseAction(s,l,t):
			return opening + self.wikiMarkup.transformString (prefix + t[0] + suffix) + closing
		return conversionParseAction


	def __convertToText (self, text):
		def conversionParseAction(s,l,t):
			return text
		return conversionParseAction


	def __convertToHeading (self, opening, closing):
		def conversionParseAction(s,l,t):
			return opening + t["title"] + closing
		return conversionParseAction

	
	def __convertLinkArrow (self, text):
		"""
		Преобразовать ссылки в виде [[comment -> url]]
		"""
		comment, url = text.split ("->")
		realurl = self.__prepareUrl (url)

		return self.__getUrlTag (realurl, comment)


	def __convertLinkLine (self, text):
		"""
		Преобразовать ссылки в виде [[url | comment]]
		"""
		url, comment = text.split ("|")
		realurl = self.__prepareUrl (url)

		return self.__getUrlTag (realurl, comment)


	def __prepareUrl (self, url):
		"""
		Подготовить адрес для ссылки. Если ссылка - прикрепленный файл, то создать путь до него
		"""
		if url.strip().startswith (self.__attachString):
			return url.strip().replace (self.__attachString, RootWikiPage.attachDir + "/", 1)

		return url


	def __getUrlTag (self, url, comment):
		return '<A HREF="%s">%s</A>' % (url.strip(), self.linkMarkup.transformString (comment.strip()) )


	def __convertEmptyLink (self, text):
		"""
		Преобразовать ссылки в виде [[link]]
		"""
		textStrip = text.strip()

		if textStrip.startswith (self.__attachString) and self.__isImage (textStrip):
			# Ссылка на прикрепленную картинку
			url = textStrip.replace (self.__attachString, RootWikiPage.attachDir + "/", 1)
			comment = self.linkMarkup.transformString (text.strip())

		elif textStrip.startswith (self.__attachString):
			# Ссылка на прикрепление, но не картинку
			url = textStrip.replace (self.__attachString, RootWikiPage.attachDir + "/", 1)
			comment = textStrip.replace (self.__attachString, "")

		else:
			# Ссылка не на прикрепление
			url = text.strip()
			comment = self.linkMarkup.transformString (text.strip())

		return '<A HREF="%s">%s</A>' % (url, comment)


	def __convertToLink (self, s, l, t):
		"""
		Преобразовать ссылку
		"""
		if "->" in t[0]:
			return self.__convertLinkArrow (t[0])
		elif "|" in t[0]:
			return self.__convertLinkLine (t[0])

		return self.__convertEmptyLink (t[0])


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


	def __convertPreformat (self, s, l, t):
		return u"<PRE>" + t[0] + u"</PRE>"


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


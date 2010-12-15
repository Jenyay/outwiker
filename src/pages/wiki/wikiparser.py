#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import os
import wx

from libs.pyparsing import QuotedString, Regex, Empty, Literal, replaceWith, LineStart, LineEnd, OneOrMore, ZeroOrMore, NotAny, Or, Optional, StringEnd
from core.tree import RootWikiPage

def replaceBreakes (text):
	lineBrake = u"[[<<]]"
	doubleBrake = "\\\\\\"

	result = text.replace (doubleBrake, "\n\n")
	result = result.replace (lineBrake, "\n")
	return result


def noConvert (s, l, t):
	return t[0]


class ThumbException (Exception):
	def __init__ (self, value):
		self.value = value


	def __str__(self):
		return self.value



class ListParams (object):
	"""
	Параметры списков в парсере
	"""
	def __init__ (self, symbol, startTag, endTag):
		self.symbol = symbol
		self.startTag = startTag
		self.endTag = endTag


class ListParser (object):
	"""
	Класс для разбора списков
	"""
	def __init__ (self, allListsParams, listItemMarkup):
		self.allListsParams = allListsParams
		self.listItemMarkup = listItemMarkup


	def __addDeeperLevel (self, depth, item, currItem):
		"""
		Создать список более глубокого уровня
		depth - разница между новым урвонем и текущим
		item - разобранный элемент строки
		currItem - список вложенных списков (их первых символов для определения типа)
		"""
		result = u""
		for _ in range (depth):
			result += self.__getStartListTag(item[0], self.allListsParams)
			currItem.append (item[0])

		return result
	

	def __closeLists (self, depth, currItem):
		"""
		Закрыть один или несколько уровней списков (перейти выше)
		depth - разность между текущим уровнем и новым урвонем
		"""
		result = u""
		for _ in range (depth):
			result += self.__getEndListTag(currItem[-1], self.allListsParams)
			del currItem[-1]

		return result
	
	
	def __closeListStartList (self, level, item, currItem):
		result = u""

		result += self.__closeLists (1, currItem)
		result += self.__getStartListTag(item[0], self.allListsParams)
		currItem.append (item[0])

		result += self.__getListItemTag (item, level, self.listItemMarkup)

		return result


	def toHtml (self, items):
		"""
		Преобразовать список элементов списка в HTML-список (возможно, вложенный)
		"""
		currLevel = 0
		currItem = []

		result = u""

		for item in items:
			if len (item.strip()) == 0:
				continue

			level = self.__getListLevel (item, self.allListsParams)

			if level == currLevel and len (currItem) > 0 and item[0] == currItem[-1]:
				# Новый элемент в текущем списке
				result += self.__getListItemTag (item, level, self.listItemMarkup)

			elif level > currLevel:
				# Более глубокий уровень
				result += self.__addDeeperLevel (level - currLevel, item, currItem)
				result += self.__getListItemTag (item, level, self.listItemMarkup)

			elif level < currLevel:
				# Более высокий уровень, но тот же тип списка
				result += self.__closeLists (currLevel - level, currItem)

				if item[0] == currItem[-1]:
					result += self.__getListItemTag (item, level, self.listItemMarkup)
				else:
					result += self.__closeListStartList (level, item, currItem)

			elif level == currLevel and len (currItem) > 0 and item[0] != currItem[-1]:
				# Тот же уровень, но другой список
				result += self.__closeListStartList (level, item, currItem)

			else:
				assert False

			currLevel = level

		result += self.__closeLists (currLevel, currItem)

		return result


	def getListToken (self):
		regex = "(?P<level>["

		for param in self.allListsParams:
			regex += param.symbol

		regex += "]+) *(?P<item>.*)"

		item =  LineStart() + Regex (regex).setParseAction (noConvert) + LineEnd()

		fullList = OneOrMore (item).setParseAction (self.__convertList)

		return fullList


	def __convertList (self, s, loc, tokens):
		"""
		Преобразовать список элементов списка в HTML-список (возможно, вложенный)
		"""
		return self.toHtml (tokens)


	def __getListLevel (self, item, params):
		"""
		Получить уровень списка по его элементу (количество символов # и * в начале строки)
		"""
		found = False
		for param in params:
			if item[0] == param.symbol:
				found = True
				break

		if not found:
			return 0

		level = 1
		while level < len (item) and item[level] == item[0]:
			level += 1

		return level


	def __getListItemTag (self, item, level, listItemMarkup):
		text = (item[level:]).strip()
		itemText = listItemMarkup.transformString (replaceBreakes (text) )

		return u"<LI>%s</LI>" % (itemText)
	

	def __getStartListTag (self, symbol, params):
		"""
		Получить открывающийся тег для элемента
		"""
		for listparam in params:
			if listparam.symbol == symbol:
				return listparam.startTag
	

	def __getEndListTag (self, symbol, params):
		"""
		Получить закрывающийся тег для элемента
		"""
		for listparam in params:
			if listparam.symbol == symbol:
				return listparam.endTag



class Parser (object):
	def __init__ (self, page, maxSizeThumb = 250):
		self.page = page

		# Имя файла превьюшки: th_width_200_fname
		# Имя файла превьюшки: th_height_100_fname
		self.thumbsTemplate = "th_%s_%d_%s"

		self.thumbsDir = "__thumb"
		self._configSection = u"Wikiparser"
		self.maxsizeThumbDefault = 250
		
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

		self.maxSizeThumb = maxSizeThumb
		
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
		self.thumb = self.__getThumbsToken ()
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

	
	def __getThumbsWidth (self):
		result = Regex (r"""% *?(thumb +)?width *?= *?(?P<width>\d+) *?(px)? *?% *?Attach:(?P<fname>.*?\.(jpe?g|bmp|gif|tiff?|png)) *?%%""")
		result.setParseAction (self.__convertThumbWidth)
		return result


	def __getThumbsToken (self):
		result = Regex (r"""% *?(((thumb +)?width *?= *?(?P<width>\d+) *?(px)?)|((thumb +)?height *?= *?(?P<height>\d+) *?(px)?)|((thumb +)?maxsize *?= *?(?P<maxsize>\d+) *?(px)?)|(thumb *?)) *?% *?Attach:(?P<fname>.*?\.(jpe?g|bmp|gif|tiff?|png)) *?%%""")
		result.setParseAction (self.__convertThumb)
		return result


	def __convertToImage (self, s, l, t):
		return u'<IMG SRC="%s">' % t[0]

	
	def __getNotImageAttachTokens (self):
		"""
		Создать элементы из прикрепленных файлов.
		Отдельно картинки, отдельно все файлы
		"""
		attachesAll = []

		attaches = self.page.attachment

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


	def __getImageAttachTokens (self):
		"""
		Создать элементы из прикрепленных файлов.
		Отдельно картинки, отдельно все файлы
		"""
		attachesImages = []

		attaches = self.page.attachment

		for attach in attaches:
			if self.__isImage (attach):
				fname = os.path.basename (attach)
				attach_token = self.__attachString + Literal (fname)
				attach_token.setParseAction (replaceWith (self.__getReplaceForImageAttach (fname) ) )
				attachesImages.append (attach_token)

		return attachesImages

	
	def __isImage (self, fname):
		images_ext = [".png", ".bmp", ".gif", ".tif", ".tiff", ".jpg", ".jpeg"]

		for ext in images_ext:
			if fname.lower().endswith (ext):
				return True

		return False
		

	def __convertToHTML(self, opening,closing):
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


	def __convertThumb (self, s, l, t):
		if t["width"] != None:
			return self.__convertThumbWidth (s, l, t)
		elif t["height"] != None:
			return self.__convertThumbHeight (s, l, t)
		elif t["maxsize"] != None:
			return self.__convertThumbMaxSize (s, l, t)
		else:
			return self.__convertThumbDefault (s, l, t)


	def __convertThumbWidth (self, s, l, t):
		try:
			width = int (t["width"])
		except ValueError:
			return u"<b>Width error</b>"

		fname = t["fname"]

		path = os.path.join (self.page.path, RootWikiPage.attachDir, self.thumbsDir)
		if not os.path.exists (path):
			try:
				os.mkdir (path)
			except:
				return u"<b>Can't create folder %s</b>" % path

		path_src = os.path.join (self.page.path, RootWikiPage.attachDir, fname)

		fname_res = self.thumbsTemplate % ("width", width, fname)

		# wx не умеет сохранять в GIF, поэтому преобразуем в PNG
		if fname_res.lower().endswith (".gif"):
			fname_res = fname_res.replace (".gif", ".png")

		path_res = os.path.join (self.page.path, RootWikiPage.attachDir, self.thumbsDir, fname_res)

		try:
			self.__makeThumbByWidth (path_src, width, path_res)

		except ThumbException as e:
			return u"<B>" + e.value + u"</B>"

		except Exception as e:
			return u"<B>" + repr (e) + u"</B>"

		return u'<A HREF="%s/%s"><IMG SRC="%s/%s/%s"></A>' % (RootWikiPage.attachDir, fname, 
				RootWikiPage.attachDir, self.thumbsDir, fname_res)


	def __convertThumbHeight (self, s, l, t):
		try:
			height = int (t["height"])
		except ValueError:
			return u"<b>Height error</b>"

		fname = t["fname"]

		path = os.path.join (self.page.path, RootWikiPage.attachDir, self.thumbsDir)
		if not os.path.exists (path):
			try:
				os.mkdir (path)
			except:
				return u"<b>Can't create folder %s</b>" % path

		path_src = os.path.join (self.page.path, RootWikiPage.attachDir, fname)

		fname_res = self.thumbsTemplate % ("height", height, fname)

		# wx не умеет сохранять в GIF, поэтому преобразуем в PNG
		if fname_res.lower().endswith (".gif"):
			fname_res = fname_res.replace (".gif", ".png")

		path_res = os.path.join (self.page.path, RootWikiPage.attachDir, self.thumbsDir, fname_res)

		try:
			self.__makeThumbByHeight (path_src, height, path_res)

		except ThumbException as e:
			return u"<B>" + e.value + u"</B>"

		except Exception as e:
			return u"<B>" + unicode (e) + u"</B>"

		return '<A HREF="%s/%s"><IMG SRC="%s/%s/%s"></A>' % (RootWikiPage.attachDir, fname, 
				RootWikiPage.attachDir, self.thumbsDir, fname_res)
	

	def __convertThumbDefault (self, s, l, t):
		fname = t["fname"]

		path = os.path.join (self.page.path, RootWikiPage.attachDir, self.thumbsDir)
		if not os.path.exists (path):
			try:
				os.mkdir (path)
			except:
				return u"<b>Can't create folder %s</b>" % path

		path_src = os.path.join (self.page.path, RootWikiPage.attachDir, fname)

		fname_res = self.thumbsTemplate % ("maxsize", self.maxSizeThumb, fname)

		# wx не умеет сохранять в GIF, поэтому преобразуем в PNG
		if fname_res.lower().endswith (".gif"):
			fname_res = fname_res.replace (".gif", ".png")

		path_res = os.path.join (self.page.path, RootWikiPage.attachDir, self.thumbsDir, fname_res)

		try:
			self.__makeThumbByMaxSize (path_src, self.maxSizeThumb, path_res)
		
		except ThumbException as e:
			return u"<B>" + e.value + u"</B>"

		except Exception as e:
			return u"<B>" + unicode (e) + u"</B>"

		return '<A HREF="%s/%s"><IMG SRC="%s/%s/%s"></A>' % (RootWikiPage.attachDir, fname, 
				RootWikiPage.attachDir, self.thumbsDir, fname_res)
	

	def __convertThumbMaxSize (self, s, l, t):
		try:
			maxsize = int (t["maxsize"])
		except ValueError:
			return u"<b>Maxsize error</b>"

		fname = t["fname"]

		path = os.path.join (self.page.path, RootWikiPage.attachDir, self.thumbsDir)
		if not os.path.exists (path):
			try:
				os.mkdir (path)
			except:
				return u"<b>Can't create folder %s</b>" % path

		path_src = os.path.join (self.page.path, RootWikiPage.attachDir, fname)

		fname_res = self.thumbsTemplate % ("maxsize", maxsize, fname)

		# wx не умеет сохранять в GIF, поэтому преобразуем в PNG
		if fname_res.lower().endswith (".gif"):
			fname_res = fname_res.replace (".gif", ".png")

		path_res = os.path.join (self.page.path, RootWikiPage.attachDir, self.thumbsDir, fname_res)

		try:
			self.__makeThumbByMaxSize (path_src, maxsize, path_res)
		
		except ThumbException as e:
			return u"<B>" + e.value + u"</B>"

		except Exception as e:
			return u"<B>" + unicode (e) + u"</B>"

		return '<A HREF="%s/%s"><IMG SRC="%s/%s/%s"></A>' % (RootWikiPage.attachDir, fname, 
				RootWikiPage.attachDir, self.thumbsDir, fname_res)


	def __makeThumbByWidth (self, fname_src, width_res, fname_res):
		"""
		Создать превьюшку определенной ширины
		"""
		if not os.path.exists (fname_src):
			raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src) )

		image_src = wx.Image (fname_src)
		width_src = image_src.GetWidth()
		height_src = image_src.GetHeight()

		scale = float (width_res) / float (width_src)
		height_res = int (height_src * scale)

		image_src.Rescale (width_res, height_res, wx.IMAGE_QUALITY_HIGH)
		image_src.SaveFile (fname_res, self.__getImageType (fname_res) )
	

	def __makeThumbByHeight (self, fname_src, height_res, fname_res):
		"""
		Создать превьюшку определенной высоты
		"""
		if not os.path.exists (fname_src):
			raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src) )

		image_src = wx.Image (fname_src)
		width_src = image_src.GetWidth()
		height_src = image_src.GetHeight()

		scale = float (height_res) / float (height_src)
		width_res = int (width_src * scale)

		image_src.Rescale (width_res, height_res, wx.IMAGE_QUALITY_HIGH)
		image_src.SaveFile (fname_res, self.__getImageType (fname_res) )
	

	def __makeThumbByMaxSize (self, fname_src, maxsize_res, fname_res):
		"""
		Создать превьюшку с заданным максимальным размером
		"""
		if not os.path.exists (fname_src):
			raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src) )

		image_src = wx.Image (fname_src)

		width_src = image_src.GetWidth()
		height_src = image_src.GetHeight()

		if width_src > height_src:
			self.__makeThumbByWidth (fname_src, maxsize_res, fname_res)
		else:
			self.__makeThumbByHeight (fname_src, maxsize_res, fname_res)

	

	def __getImageType (self, fname):
		if fname.lower().endswith (".jpg") or fname.lower().endswith (".jpeg"):
			return wx.BITMAP_TYPE_JPEG

		if fname.lower().endswith (".bmp"):
			return wx.BITMAP_TYPE_BMP

		if fname.lower().endswith (".png"):
			return wx.BITMAP_TYPE_PNG

		if fname.lower().endswith (".tif") or fname.lower().endswith (".tiff"):
			return wx.BITMAP_TYPE_TIF
	

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


	def toCompleteHtml (self, text):
		"""
		Сгенерить HTML полностью
		"""
		template = u"<html><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/></head><body>%s</body></html>"

		text = text.replace ("\r\n", "\n")

		text = self.__replaceEndlines (self.toHtml (text) )

		text = template % text

		return text


	def __replaceEndlines (self, text):
		"""
		Заменить переводы строк, но не трогать текст внутри <PRE>...</PRE>
		"""
		text_lower = text.lower()

		starttag = "<pre>"
		endtag = "</pre>"

		# Разобьем строку по <pre>
		part1 = text_lower.split (starttag)

		# Подстроки разобьем по </pre>
		parts2 = [item.split (endtag) for item in part1]

		# Склеим части в один массив
		parts = reduce (lambda x, y: x + y, parts2, [])

		# В четных элементах массива заменим переводы строк, а нечетные оставим как есть
		# Строки берем из исходного текста с учетом пропущенных в массиве тегов <pre> и </pre>
		result = u""
		index = 0

		for n in range (len (parts)):
			item = text[index: index + len (parts[n]) ]
			if n % 2 == 0:
				item = item.replace ("\n\n", "<p>")
				item = item.replace ("\n", "<br>")
				item = item.replace ("<br><li>", "<li>")
				index += len (parts[n]) + len (starttag)
			else:
				item = "<PRE>" + item + "</PRE>"
				index += len (parts[n]) + len (endtag)

			result += item

		return result



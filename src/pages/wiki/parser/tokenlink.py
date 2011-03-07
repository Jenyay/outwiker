#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from libs.pyparsing import QuotedString

from tokenattach import AttachToken
from utils import isImage
from core.tree import RootWikiPage


class LinkFactory (object):
	@staticmethod
	def make (parser):
		return LinkToken(parser).getToken()


class LinkToken (object):
	linkStart = "[["
	linkEnd = "]]"
	attachString = u"Attach:"

	def __init__ (self, parser):
		self.parser = parser


	def getToken (self):
		return QuotedString(LinkToken.linkStart, 
				endQuoteChar = LinkToken.linkEnd, 
				multiline = True).setParseAction(self.__convertToLink)
	

	def __convertToLink (self, s, l, t):
		"""
		Преобразовать ссылку
		"""
		if "->" in t[0]:
			return self.__convertLinkArrow (t[0])
		elif "|" in t[0]:
			return self.__convertLinkLine (t[0])

		return self.__convertEmptyLink (t[0])


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
		if url.strip().startswith (AttachToken.attachString):
			return url.strip().replace (AttachToken.attachString, RootWikiPage.attachDir + "/", 1)

		return url


	def __getUrlTag (self, url, comment):
		return '<A HREF="%s">%s</A>' % (url.strip(), self.parser.parseLinkMarkup (comment.strip()) )


	def __convertEmptyLink (self, text):
		"""
		Преобразовать ссылки в виде [[link]]
		"""
		textStrip = text.strip()

		if textStrip.startswith (AttachToken.attachString) and isImage (textStrip):
			# Ссылка на прикрепленную картинку
			url = textStrip.replace (AttachToken.attachString, RootWikiPage.attachDir + "/", 1)
			comment = self.parser.parseLinkMarkup (text.strip())

		elif textStrip.startswith (AttachToken.attachString):
			# Ссылка на прикрепление, но не картинку
			url = textStrip.replace (AttachToken.attachString, RootWikiPage.attachDir + "/", 1)
			comment = textStrip.replace (AttachToken.attachString, "")

		else:
			# Ссылка не на прикрепление
			url = text.strip()
			comment = self.parser.parseLinkMarkup (text.strip())

		return '<A HREF="%s">%s</A>' % (url, comment)

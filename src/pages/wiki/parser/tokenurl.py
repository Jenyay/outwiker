#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from libs.pyparsing import Regex

from utils import noConvert


class UrlFactory (object):
	@staticmethod
	def make (parser):
		return UrlToken(parser).getToken()


class UrlToken (object):
	def __init__ (self, parser):
		self.parser = parser


	def getToken (self):
		token =  Regex ("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)\\.)[-A-Za-z0-9\\.]+[-A-Za-z0-9]+)(:[0-9]*)?(/([-A-Za-z0-9_,\\$\\.\\+\\!\\*\\(\\):@|&=\\?/~\\#\\%]*[-A-Za-z0-9_\\$\\+\\!\\*\\(\\):@|&=\\?/~\\#\\%])?)?", re.IGNORECASE)

		token.setParseAction(self.__convertToUrlLink)
		return token


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


	def __getUrlTag (self, url, comment):
		return '<A HREF="%s">%s</A>' % (url.strip(), self.parser.parseLinkMarkup (comment.strip()) )

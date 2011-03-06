#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from libs.pyparsing import Regex


class UrlImageFactory (object):
	@staticmethod
	def make (parser):
		return UrlImageToken(parser).getToken()


class UrlImageToken (object):
	"""
	Токен для горизонтальной линии
	"""
	def __init__ (self, parser):
		self.parser = parser


	def getToken (self):
		token = Regex ("(https?|ftp)://[a-z0-9-]+(\.[a-z0-9-]+)+(/[-._\w%]+)*/[-\w_.%]+\.(gif|png|jpe?g|bmp|tiff?)", re.IGNORECASE)
		token.setParseAction(lambda s, l, t: u'<IMG SRC="%s">' % t[0])
		return token


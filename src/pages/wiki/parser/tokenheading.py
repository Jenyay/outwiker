#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from libs.pyparsing import Regex


class HeadingFactory (object):
	@staticmethod
	def make (parser):
		return HeadingToken().getToken()


class HeadingToken (object):
	def __init__ (self):
		self.heading_Regex = "^(?P<header>!!+)\s+(?P<title>.*)$"


	def getToken (self):
		"""
		Токены для заголовков H1, H2,...
		"""
		return Regex (self.heading_Regex, re.MULTILINE).setParseAction(self.convertToHeading)


	def convertToHeading (s, l, t):
		level = len (t["header"]) - 1
		return u"<H%d>%s</H%d>" % (level, t["title"], level)


	def __convertToHeading (self, opening, closing):
		def conversionParseAction(s,l,t):
			return opening + t["title"] + closing
		return conversionParseAction

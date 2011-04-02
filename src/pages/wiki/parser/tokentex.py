#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import hashlib
import os
import os.path
import subprocess

from libs.pyparsing import QuotedString
from core.tree import RootWikiPage
from core.system import getOS
from ..texrender import getTexRender
from ..thumbnails import Thumbnails

class TexFactory (object):
	@staticmethod
	def make (parser):
		return TexToken(parser).getToken()


class TexToken (object):
	"""
	Класс токена для разбора формул
	"""
	texStart = "{$"
	texEnd = "$}"

	def __init__ (self, parser):
		self.parser = parser


	def getToken (self):
		return QuotedString (TexToken.texStart, 
				endQuoteChar = TexToken.texEnd, 
				multiline = True).setParseAction(self.makeTexEquation)


	def makeTexEquation (self, s, l, t):
		eqn = t[0].strip()

		thumb = Thumbnails(self.parser.page)

		try:
			path = thumb.getThumbPath (True)
		except IOError:
			return _(u"<B>Can't create thumbnails directory</B>")

		tex = getTexRender (path)

		try:
			image_fname = tex.makeImage (eqn)
		except IOError:
			return _(u"<B>Can't create imege file</B>")
		
		image_path = os.path.join (Thumbnails.getRelativeThumbDir(), image_fname)
		result = u'<IMG SRC="{image}">'.format (image=image_path)

		return result


#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import hashlib
import os
import os.path

from libs.pyparsing import QuotedString
from core.tree import RootWikiPage

from ..texconfig import TexConfig


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
		self.tempFname = "__eqn.tex"


	def getToken (self):
		return QuotedString (TexToken.texStart, 
				endQuoteChar = TexToken.texEnd, 
				multiline = True).setParseAction(self.makeTexEquation)


	def makeTexEquation (self, s, l, t):
		eqn = t[0].strip()

		md5 = hashlib.md5 (eqn).hexdigest()

		path = os.path.join (self.parser.page.getAttachPath(True), "__thumb")
		fname = u"eqn_{0}.gif".format (md5)
		fname_full = os.path.join (path, fname)

		if not os.path.exists (path):
			try:
				os.mkdir (path)
			except IOError:
				return _(u"<B>Can't create directory %s</B>" % path)


		temp_fname = os.path.join (path, self.tempFname)
		try:
			with open (temp_fname, "w") as fp:
				fp.write (eqn)
		except IOError:
			return _(u"<B>Can't create file %s</B>" % temp_fname)


		try:
			self.makeTexImage (temp_fname, fname_full)
		except IOError:
			return _(u"<B>Can't create file %s</B>" % fname_full)

		
		image_path = os.path.join (RootWikiPage.attachDir, "__thumb", fname)
		result = u'<IMG SRC="{image}">'.format (image=image_path)

		return result


	def makeTexImage (self, eqn_fname, fname):
		texconfig = TexConfig (self.parser.config)
		mimeTexPath = texconfig.mimeTexPath.value

		path = u'"{mimetex}" -f "{eqn_fname}" -e "{fname_out}" {params}'.format (mimetex=mimeTexPath, 
				eqn_fname=eqn_fname, 
				fname_out=fname,
				params="")

		# TODO: Проверить как это работает в винде
		pipe = os.popen(path.encode ("utf8"))
		pipe.read()
		pipe.close()

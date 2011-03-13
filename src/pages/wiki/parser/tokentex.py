#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import hashlib
import os
import os.path
import subprocess

from libs.pyparsing import QuotedString
from core.tree import RootWikiPage
from core.system import getOS

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
		self.tempFname = "__temp.tmp"


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


	def makeTexImage (self, fname_eqn, fname_image):
		currentOS = getOS()

		mimeTexPath = currentOS.mimeTexPathDefault

		p = subprocess.Popen([mimeTexPath.encode (currentOS.filesEncoding), 
			"-f", fname_eqn.encode (currentOS.filesEncoding), 
			"-e", fname_image.encode (currentOS.filesEncoding)], shell=True)

		p.communicate()

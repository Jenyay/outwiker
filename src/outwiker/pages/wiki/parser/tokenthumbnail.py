#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import Regex

from outwiker.core.thumbexception import ThumbException
from pagethumbmaker import PageThumbmaker
from outwiker.core.attachment import Attachment
from ..wikiconfig import WikiConfig


class ThumbnailFactory (object):
	"""
	Класс для создания токена ThumbnailToken
	"""
	@staticmethod
	def make (parser):
		return ThumbnailToken(parser).getToken()


class ThumbnailToken (object):
	"""
	Класс, содержащий все необходимое для разбора и создания превьюшек картинок на вики-странице
	"""
	def __init__ (self, parser):
		self.parser = parser
		self.thumbmaker = PageThumbmaker()
	

	def getToken (self):
		result = Regex (r"""% *?(((thumb +)?width *?= *?(?P<width>\d+) *?(px)?)|((thumb +)?height *?= *?(?P<height>\d+) *?(px)?)|((thumb +)?maxsize *?= *?(?P<maxsize>\d+) *?(px)?)|(thumb *?)) *?% *?Attach:(?P<fname>.*?\.(jpe?g|bmp|gif|tiff?|png)) *?%%""")
		result.setParseAction (self.__convertThumb)
		return result


	def __convertThumb (self, s, l, t):
		if t["width"] != None:
			try:
				size = int (t["width"])
			except ValueError:
				return _(u"<b>Width error</b>")

			func = self.thumbmaker.createThumbByWidth

		elif t["height"] != None:
			try:
				size = int (t["height"])
			except ValueError:
				return u"<b>Height error</b>"

			func = self.thumbmaker.createThumbByHeight

		elif t["maxsize"] != None:
			try:
				size = int (t["maxsize"])
			except ValueError:
				return u"<b>Maxsize error</b>"

			func = self.thumbmaker.createThumbByMaxSize

		else:
			config = WikiConfig (self.parser.config)
			size = config.thumbSizeOptions.value
			func = self.thumbmaker.createThumbByMaxSize

		fname = t["fname"]

		try:
			thumb = func (self.parser.page, fname, size)

		except ThumbException as e:
			return _(u"<b>Can't create thumbnail: \n%s</b>" % repr (e))

		except IOError as e:
			return _(u"<b>Can't create thumbnail: \n%s</b>" % repr (e))

		return u'<A HREF="%s/%s"><IMG SRC="%s"/></A>' % (Attachment.attachDir, fname, thumb.replace ("\\", "/"))

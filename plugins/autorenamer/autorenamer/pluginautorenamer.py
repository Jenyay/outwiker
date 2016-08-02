# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version

from .i18n import set_


__version__ = u"0.0.0.2"


if getCurrentVersion() < Version (1, 8, 1):
	print ("AutoRenamer plugin. OutWiker version requirement: 1.8.1")
else:
	from autorenamer import AutoRenamer

	class PluginAutoRenamer (Plugin):
		def __init__ (self, application):
			Plugin.__init__ (self, application)
			self._autorenamer = AutoRenamer(self, application)

		@property
		def name (self):
			return u"AutoRenamer"

		@property
		def description (self):
			description = _(u'''Plugin allows to rename all pages automatically using the first line of the page or automatically rename just those pages where you place (:autorename:) mark''')
			author = _(u'''<b>Author:</b> Vitalii Koshura (delionkur-lestat@mail.ru)''')
			return u"""{description}\n\n{author}""".format (description=description, author=author)

		@property
		def url (self):
			return u"https://github.com/AenBleidd/OutwikerPlugin"

		@property
		def version (self):
			return __version__

		def initialize(self):
			self._initlocale(u"AutoRenamer")
			self._autorenamer.initialize()

		def destroy(self):
			self._autorenamer.destroy()

		def _initlocale (self, domain):
			langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
			global _
			try:
				_ = self._init_i18n (domain, langdir)
			except BaseException, e:
				print e
			set_(_)

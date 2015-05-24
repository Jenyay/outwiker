# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command
from .renamer import Renamer

class AutoRenameTagCommand (Command):
	def __init__ (self, application, parser):
		Command.__init__ (self, parser)
		self._application = application
		self._renamer = Renamer(application)

	@property
	def name (self):
		return u"autorename"

	def execute (self, params, content):
		self._renamer.RenamePage(True)
		return u""

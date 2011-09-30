#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import abstractmethod
from abc import ABCMeta

import wx

import outwiker.core

class HtmlRender (wx.Panel):
	"""
	Базовый класс для HTML-рендеров
	"""
	__metaclass__ = ABCMeta

	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		self._currentPage = None


	@abstractmethod
	def LoadPage (self, fname):
		"""
		Загрузить страницу из файла
		"""
		pass


	def SetPage (self, htmltext, basepath):
		"""
		Загрузить страницу из строки
		htmltext - текст страницы
		basepath - путь до папки, относительно которой ищутся локальные ресурсы (картинки)
		"""
		pass


	@property
	def page (self):
		return self._currentPage


	@page.setter
	def page (self, value):
		self._currentPage = value


	def _isUrl (self, href):
		return href.lower().startswith ("http://") or \
				href.lower().startswith ("https://") or \
				href.lower().startswith ("ftp://") or \
				href.lower().startswith ("mailto:")


	def openUrl (self, href):
		"""
		Открыть ссылку в браузере (или почтовый адрес в почтовике)
		"""
		try:
			outwiker.core.system.getOS().startFile (href)
		except OSError:
			text = _(u"Can't execute file '%s'") % (href)
			outwiker.core.commands.MessageBox (text, "Error", wx.ICON_ERROR | wx.OK)

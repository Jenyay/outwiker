#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import urllib

import wx
import wx.lib.iewin

import core.system
import core.commands
from core.application import Application


class HtmlRenderIE (wx.Panel):
	"""
	Класс для рендеринга HTML с использованием wxWebKit под Windows (http://wxwebkit.kosoftworks.com/)
	"""
	def __init__ (self, parent, *args, **kwds):
		wx.Panel.__init__ (self, parent, *args, **kwds)

		self.render = wx.lib.iewin.IEHtmlWindow (self)

		# Подпишемся на события IE
		self.render.AddEventSink(self)

		self.canOpenUrl = False                # Можно ли открывать ссылки
		self.currentUri = None                 # Текущая открытая страница

		self.__layout()

		self._currentPage = None

		#self.render.Bind (wx.html.EVT_HTML_LINK_CLICKED, self.onLinkClicked)
		#self.render.Bind (wx.html.EVT_HTML_CELL_HOVER, self.onCellHover)
		#self.render.Bind (wx.EVT_ENTER_WINDOW, self.onMouseEnter)
		#self.render.Bind (wx.EVT_MOTION, self.onMouseMove)

		#self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_COPY)
		#self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_CUT)


	def __layout (self):
		self.box = wx.BoxSizer(wx.VERTICAL)
		self.box.Add(self.render, 1, wx.EXPAND)

		self.SetSizer(self.box)
		self.Layout()

	
	def LoadPage (self, fname):
		self.canOpenUrl = True
		self.render.Navigate (fname)
		self.canOpenUrl = False


	def _removeFileProtokol (self, href):
		"""
		Избавиться от протокола file:///, то избавимся от этой надписи
		"""
		fileprotocol = u"file:///"
		if href.startswith (fileprotocol):
			return href[len (fileprotocol): ]

		return href


	def BeforeNavigate2(self, this, pDisp, URL, Flags, TargetFrameName, PostData, Headers, Cancel):
		href = URL[0]
		curr_href = urllib.unquote ( self._removeFileProtokol (self.render.locationurl) ).replace ("/", "\\")

		if self.canOpenUrl or href == curr_href:
			Cancel[0] = False
		else:
			Cancel[0] = True
			self.currentUri = href
			self._onLinkClicked (href)


	def identifyUri (self, href):
		"""
		Определить тип ссылки и вернуть кортеж (url, page, filename)
		"""
		if self.__isUrl (href):
			return (href, None, None)

		page = self.__findWikiPage (href)
		filename = self.__findFile (href)

		return (None, page, filename)


	def _onLinkClicked (self, href):
		"""
		Клик по ссылке
		"""
		(url, page, filename) = self.identifyUri (href)

		if url != None:
			self.openUrl (url)

		elif page != None:
			self._currentPage.root.selectedPage = page

		elif filename != None:
			try:
				core.system.getOS().startFile (filename)
			except OSError:
				text = _(u"Can't execute file '%s'") % filename
				core.commands.MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)


	@property
	def page (self):
		return self._currentPage


	@page.setter
	def page (self, value):
		self._currentPage = value
	

	def __isUrl (self, href):
		return href.lower().startswith ("http://") or \
				href.lower().startswith ("https://") or \
				href.lower().startswith ("ftp://") or \
				href.lower().startswith ("mailto:")
	

	def __findFile (self, href):
		path = os.path.join (self._currentPage.path, href)
		if os.path.exists (path):
			return path


	def __findWikiPage (self, subpath):
		"""
		Попытка найти страницу вики, если ссылка, на которую щелкнули не интернетная (http, ftp, mailto)
		"""
		assert self._currentPage != None

		newSelectedPage = None

		if subpath.startswith (self._currentPage.path):
			subpath = subpath[len (self._currentPage.path) + 1: ].replace ("\\", "/")
		elif subpath[1] == ":":
			subpath = subpath[2:].replace ("\\", "/")

		if subpath[0] == "/":
			# Поиск страниц осуществляем только с корня
			newSelectedPage = self._currentPage.root[subpath[1:] ]
		else:
			# Сначала попробуем найти вложенные страницы с таким subpath
			newSelectedPage = self._currentPage[subpath]

			if newSelectedPage == None:
				# Если страница не найдена, попробуем поискать, начиная с корня
				newSelectedPage = self._currentPage.root[subpath]

		return newSelectedPage
		

	def openUrl (self, href):
		"""
		Открыть ссылку в браузере (или почтовый адрес в почтовике)
		"""
		try:
			core.system.getOS().startFile (href)
		except OSError:
			text = _(u"Can't execute file '%s'") % (href)
			core.commands.MessageBox (text, "Error", wx.ICON_ERROR | wx.OK)

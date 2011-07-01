#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import urllib

import wx
import wx.lib.iewin

from .htmlrender import HtmlRender
import core.system
import core.commands
from core.application import Application
from core.commands import MessageBox


class HtmlRenderIE (HtmlRender):
	"""
	Класс для рендеринга HTML с использованием движка IE под Windows
	"""
	def __init__ (self, parent):
		HtmlRender.__init__ (self, parent)

		self.render = wx.lib.iewin.IEHtmlWindow (self)

		# Подпишемся на события IE
		self.render.AddEventSink(self)

		self.canOpenUrl = False                # Можно ли открывать ссылки
		self.currentUri = None                 # Текущая открытая страница

		self.__layout()

		self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_COPY)
		self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_CUT)


	def Print (self):
		self.render.Print (True)


	def SetPage (self, htmltext, basepath):
		"""
		Загрузить страницу из строки
		htmltext - текст страницы
		basepath - путь, относительно которого отсчитываются относительные пути (НЕ ИСПОЛЬЗУЕТСЯ!!!)
		"""
		self.canOpenUrl = True
		self.render.LoadString (htmltext)
		self.canOpenUrl = False


	def StatusTextChange(self, status):
		if len (status) != 0:
			href = self.__cleanUpUrl (status)

			(url, page, filename) = self.identifyUri (href)

			if page != None:
				core.commands.setStatusText (page.subpath)
			elif filename != None:
				core.commands.setStatusText (filename)
			else:
				core.commands.setStatusText (status)
		else:
			core.commands.setStatusText (status)


	def onCopyFromHtml(self, event):
		document = self.render.document
		selection = document.selection

		if selection != None:
			selrange = selection.createRange()
			if selrange != None:
				core.commands.copyTextToClipboard (selrange.text)
				event.Skip()


	def __layout (self):
		self.box = wx.BoxSizer(wx.VERTICAL)
		self.box.Add(self.render, 1, wx.EXPAND)

		self.SetSizer(self.box)
		self.Layout()

	
	def LoadPage (self, fname):
		self.canOpenUrl = True
		self.render.Navigate (fname)


	def __cleanUpUrl (self, href):
		"""
		Почистить ссылку. Убрать file:/// и about:blank
		"""
		result = self._removeFileProtokol (href)
		#result = self.__removeAboutBlank (result)
		result = urllib.unquote (result)
		result = result.replace ("/", u"\\")

		return result


	def __removeAboutBlank (self, href):
		"""
		Удалить about: и about:blank из начала адреса
		"""
		about_full = u"about:blank"
		about_short = u"about:"

		result = href
		if result.startswith (about_full):
			result = result[len (about_full): ]

		elif result.startswith (about_short):
			result = result[len (about_short): ]

		return result


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
		#href = self.__cleanUpUrl (URL[0])
		curr_href = self.__cleanUpUrl (self.render.locationurl)

		if self.canOpenUrl or href == curr_href:
			Cancel[0] = False
			self.canOpenUrl = False
		else:
			Cancel[0] = True
			self.currentUri = href
			self._onLinkClicked (href)


	def identifyUri (self, href):
		"""
		Определить тип ссылки и вернуть кортеж (url, page, filename)
		"""
		if self._isUrl (href):
			return (href, None, None)

		page = self.__findWikiPage (href)
		filename = self.__findFile (href)

		return (None, page, filename)


	def _onLinkClicked (self, href):
		"""
		Клик по ссылке
		"""
		#MessageBox (href)

		(url, page, filename) = self.identifyUri (urllib.unquote (href) )

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
		elif len (subpath) > 1 and subpath[1] == ":":
			subpath = subpath[2:].replace ("\\", "/")

		if subpath.startswith ("about:"):
			subpath = self.__removeAboutBlank (subpath).replace ("\\", "/")
		
		if len (subpath) > 0 and subpath[0] == "/":
			# Поиск страниц осуществляем только с корня
			newSelectedPage = self._currentPage.root[subpath[1:] ]
		else:
			# Сначала попробуем найти вложенные страницы с таким subpath
			newSelectedPage = self._currentPage[subpath]

			if newSelectedPage == None:
				# Если страница не найдена, попробуем поискать, начиная с корня
				newSelectedPage = self._currentPage.root[subpath]

		return newSelectedPage

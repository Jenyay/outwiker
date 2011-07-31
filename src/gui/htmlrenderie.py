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
from .htmlcontrollerie import UriIdentifier


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

		self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_COPY)
		self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_CUT)


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

			#identifier = UriIdentifier ()
			(url, page, filename) = self.__identifyUri (href)

			if page != None:
				core.commands.setStatusText (page.subpath)
			elif filename != None:
				core.commands.setStatusText (filename)
			else:
				core.commands.setStatusText (status)
		else:
			core.commands.setStatusText (status)


	def __onCopyFromHtml(self, event):
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
		result = self.__removeFileProtokol (href)
		result = urllib.unquote (result)
		result = result.replace ("/", u"\\")

		return result


	def __removeFileProtokol (self, href):
		"""
		Избавиться от протокола file:///, то избавимся от этой надписи
		"""
		fileprotocol = u"file:///"
		if href.startswith (fileprotocol):
			return href[len (fileprotocol): ]

		return href


	def BeforeNavigate2 (self, this, pDisp, URL, Flags, 
			TargetFrameName, PostData, Headers, Cancel):
		href = URL[0]
		curr_href = self.__cleanUpUrl (self.render.locationurl)

		if self.canOpenUrl or href == curr_href:
			Cancel[0] = False
			self.canOpenUrl = False
		else:
			Cancel[0] = True
			self.currentUri = href
			self.__onLinkClicked (href)


	def __identifyUri (self, href):
		"""
		Определить тип ссылки и вернуть кортеж (url, page, filename)
		"""
		identifier = UriIdentifier (self._currentPage)
		return identifier.identify (href)


	def __onLinkClicked (self, href):
		"""
		Клик по ссылке
		"""
		#identifier = UriIdentifier ()
		(url, page, filename) = self.__identifyUri (urllib.unquote (href) )

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

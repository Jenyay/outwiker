#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import wx.html

import core.system
import core.commands

class HtmlView (wx.html.HtmlWindow):
	"""
	Класс для представления HTML страниц.
	"""
	def __init__ (self, *args, **kwds):
		wx.html.HtmlWindow.__init__ (self, *args, **kwds)

		self._currentPage = None

		self.Bind (wx.html.EVT_HTML_LINK_CLICKED, self.onLinkClicked)
		self.Bind (wx.html.EVT_HTML_CELL_HOVER, self.onCellHover)
		self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_COPY)
		self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_CUT)
		self.Bind (wx.EVT_ENTER_WINDOW, self.onMouseEnter)
		self.Bind (wx.EVT_MOTION, self.onMouseMove)
	

	def onCellHover (self, event):
		cell = event.GetCell()
		text = cell.GetLink().GetHref() if cell.GetLink() else u""
		core.commands.setStatusText(text)


	def onMouseMove (self, event):
		core.commands.setStatusText(u"")
		event.Skip()


	def onMouseEnter (self, event):
		self.SetFocus()

	
	def onCopyFromHtml(self, event):
		text = self.SelectionToText()
		#print text
		if len(text) == 0:
			return

		core.commands.copyTextToClipboard(text)
		event.Skip()
	

	@property
	def page (self):
		return self._currentPage


	@page.setter
	def page (self, value):
		self._currentPage = value
	

	def onLinkClicked (self, event):
		"""
		Клик по ссылке
		"""
		info = event.GetLinkInfo()
		href = info.GetHref()

		if self.__isUrl (href):
			self.openUrl (href)
		else:
			page = self.__findWikiPage (href)
			file = self.__findFile (href)

			if page != None:
				self._currentPage.root.selectedPage = page
			elif file != None:
				try:
					core.system.getOS().startFile (file)
				except OSError:
					text = _(u"Can't execute file '%s'") % file
					core.commands.MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)

	

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

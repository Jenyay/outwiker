#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import urllib

import wx

import gobject
gobject.threads_init()

import pygtk
pygtk.require('2.0')
import gtk, gtk.gdk

# pywebkitgtk (http://code.google.com/p/pywebkitgtk/)
import webkit

import core.system
import core.commands
from core.application import Application

'''
As far as I know (I may be wrong), a wx.Panel is "composed" by a GtkPizza
as a child of GtkScrolledWindow. GtkPizza is a custom widget created for
wxGTK.

WebKitGTK+ - the webkit port for GTK+ that has python bindings - wants a
GtkScrolledWindow as parent.

So all we need to embed webkit in wxGTK is find the wx.Panel's
GtkScrolledWindow.
This is acomplished using pygtk that is present in major distro's by
default, at least those that use gnome as its main desktop environment.

A last note is that for get a handle of a window in X, the window must be
"realized" first, in other words, must already exists. So we must Show
the wx.Frame before use this WKHtmlWindow class.

'''

from .htmlrender import HtmlRender


class HtmlRenderWebKit(HtmlRender):
	def __init__(self, parent):
		HtmlRender.__init__(self, parent)

		# Here is where we do the "magic" to embed webkit into wxGTK.
		whdl = self.GetHandle()

		window = gtk.gdk.window_lookup(whdl)

		# We must keep a reference of "pizza". Otherwise we get a crash.
		self.pizza = pizza = window.get_user_data()

		self.scrolled_window = scrolled_window = pizza.parent

		# Removing pizza to put a webview in it's place
		scrolled_window.remove(pizza)

		self.ctrl = ctrl = webkit.WebView()
		scrolled_window.add(ctrl)

		scrolled_window.show_all()

		self.canOpenUrl = False                # Можно ли открывать ссылки
		self.currentUri = None                 # Текущая открытая страница

		self.ctrl.connect("navigation-policy-decision-requested", self._onNavigate)
		self.ctrl.connect("hovering-over-link", self._onHoveredOverLink)
		#self.ctrl.connect("populate-popup", self._on_populate_popup)

		self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_COPY)
		self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_CUT)
		

		#self.ctrl.set_zoom_level (0.8)

	def Print (self):
		self.ctrl.get_main_frame().print_()


	def LoadPage (self, fname):
		self.canOpenUrl = True
		self.ctrl.load_uri("file://{0}".format (fname) )
		self.canOpenUrl = False


	def SetPage (self, htmltext, basepath):
		self.canOpenUrl = True
		path = "file://" + urllib.quote (basepath.encode ("utf8")) + "/"

		self.ctrl.load_string (htmltext, "text/html", "utf8", path)
		self.canOpenUrl = False


	def onCopyFromHtml(self, event):
		self.ctrl.copy_clipboard ()
		event.Skip()


	#def _on_populate_popup (self, view, menu):
	#	for i in menu.get_children():
	#		action = i.get_children()[0].get_label()
	#		print i.get_children()[0]["id"]



	def identifyUri (self, href):
		"""
		Определить тип ссылки и вернуть кортеж (url, page, filename)
		"""
		if self._isUrl (href):
			return (href, None, None)

		href_clear = self._removeFileProtokol (href)

		page = self.__findWikiPage (href_clear)
		filename = self.__findFile (href_clear)

		return (None, page, filename)


	def _onHoveredOverLink (self, view, title, uri):
		if uri == None:
			core.commands.setStatusText (u"")
			return

		href = urllib.unquote (unicode (uri, "utf8") )

		(url, page, filename) = self.identifyUri (href)

		if url != None:
			core.commands.setStatusText (url)
			return

		if page != None:
			core.commands.setStatusText (page.subpath)
			return

		if filename != None:
			core.commands.setStatusText (filename)
			return

		core.commands.setStatusText (u"")


	def _onNavigate (self, view, frame, request, action, decision):
		href = unicode (urllib.unquote (request.get_uri()), "utf8")
		curr_href = self.ctrl.get_main_frame().get_uri()

		if self.canOpenUrl or href == curr_href:
			# Если вызов uri осуществляется из программы или это запрос на обновление, то 
			# разрешить обработать запрос компоненту 
			return False
		else:
			self.currentUri = request.get_uri()
			self._onLinkClicked (href)
			return True


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


	def _removeFileProtokol (self, href):
		"""
		Так как WebKit к адресу без протокола прибавляет file://, то избавимся от этой надписи
		"""
		fileprotocol = u"file://"
		if href.startswith (fileprotocol):
			return href[len (fileprotocol): ]

		return href

	
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
			subpath = subpath[len (self._currentPage.path) + 1: ]

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

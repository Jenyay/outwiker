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
class HtmlRenderWebKit(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

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

		self._currentPage = None

		self.canOpenUrl = False                # Можно ли открывать ссылки
		self.ctrl.connect("navigation-policy-decision-requested",
                    self._onNavigate)


	# Some basic usefull methods
	#def SetEditable(self, editable=True):
	#	self.ctrl.set_editable(editable)

	def LoadPage (self, fname):
		self.canOpenUrl = True
		self.ctrl.load_uri("file://{0}".format (fname) )
		self.canOpenUrl = False


	@property
	def page (self):
		return self._currentPage


	@page.setter
	def page (self, value):
		self._currentPage = value


	def _onNavigate (self, view, frame, request, action, decision):
		if self.canOpenUrl:
			return False
		else:
			href = unicode (urllib.unquote (request.get_uri()), "utf8")
			self._onLinkClicked (href)
			return True


	def _onLinkClicked (self, href):
		"""
		Клик по ссылке
		"""
		if self.__isUrl (href):
			self.openUrl (href)
		else:
			href_clear = self._removeFileProtokol (href)

			page = self.__findWikiPage (href_clear)
			filename = self.__findFile (href_clear)

			if page != None:
				self._currentPage.root.selectedPage = page
			elif filename != None:
				print filename

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
		

	def openUrl (self, href):
		"""
		Открыть ссылку в браузере (или почтовый адрес в почтовике)
		"""
		try:
			core.system.getOS().startFile (href)
		except OSError:
			text = _(u"Can't execute file '%s'") % (href)
			core.commands.MessageBox (text, "Error", wx.ICON_ERROR | wx.OK)

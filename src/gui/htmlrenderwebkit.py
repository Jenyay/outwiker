#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import urllib

import wx

#import gobject
#gobject.threads_init()

#import pygtk
#pygtk.require('2.0')
import gtk, gtk.gdk

# pywebkitgtk (http://code.google.com/p/pywebkitgtk/)
import webkit

import core.system
import core.commands
from core.application import Application
from .htmlcontrollerwebkit import UriIdentifierWebKit

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

		self.ctrl.connect("navigation-policy-decision-requested", self.__onNavigate)
		self.ctrl.connect("hovering-over-link", self.__onHoveredOverLink)
		#self.ctrl.connect("populate-popup", self._on_populate_popup)

		self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_COPY)
		self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_CUT)
		

	def Print (self):
		self.ctrl.get_main_frame().print_()


	def LoadPage (self, fname):
		self.canOpenUrl = True

		try:
			with open (fname) as fp:
				text = fp.read()
		except IOError:
			text = _(u"Can't read file %s") % (fname)

		self.SetPage (text, os.path.dirname (fname))
		self.canOpenUrl = False


	def SetPage (self, htmltext, basepath):
		self.canOpenUrl = True
		path = "file://" + urllib.quote (basepath.encode ("utf8")) + "/"

		self.ctrl.load_string (htmltext, "text/html", "utf8", path)
		self.canOpenUrl = False


	def __onCopyFromHtml(self, event):
		self.ctrl.copy_clipboard ()
		event.Skip()


	#def _on_populate_popup (self, view, menu):
	#	for i in menu.get_children():
	#		action = i.get_children()[0].get_label()
	#		print i.get_children()[0]["id"]



	def __identifyUri (self, href):
		"""
		Определить тип ссылки и вернуть кортеж (url, page, filename)
		"""
		basepath = unicode (self.ctrl.get_main_frame().get_uri(), "utf8")
		identifier = UriIdentifierWebKit (self._currentPage, basepath)

		#print basepath
		#print href

		return identifier.identify (href)


	def __onHoveredOverLink (self, view, title, uri):
		if uri == None:
			core.commands.setStatusText (u"")
			return

		href = unicode (urllib.unquote (uri), "utf8")

		(url, page, filename, anchor) = self.__identifyUri (href)

		if url != None:
			core.commands.setStatusText (url)
			return

		if page != None:
			core.commands.setStatusText (page.subpath)
			return

		if filename != None:
			core.commands.setStatusText (filename)
			return

		if anchor != None:
			core.commands.setStatusText (anchor)
			return

		core.commands.setStatusText (u"")


	def __onNavigate (self, view, frame, request, action, decision):
		href = unicode (urllib.unquote (request.get_uri()), "utf8")
		curr_href = self.ctrl.get_main_frame().get_uri()

		if self.canOpenUrl or href == curr_href:
			# Если вызов uri осуществляется из программы или это запрос на обновление, то 
			# разрешить обработать запрос компоненту 
			return False
		else:
			return self.__onLinkClicked (href)


	def __onLinkClicked (self, href):
		"""
		Клик по ссылке
		Возвращает False, если обрабатывать ссылку разрешить компоненту, 
		в противном случае - True
		"""
		#print href
		(url, page, filename, anchor) = self.__identifyUri (href)

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

		elif anchor != None:
			return False

		return True

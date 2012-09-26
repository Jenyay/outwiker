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
# http://webkitgtk.org/reference/webkitgtk/stable/webkitgtk-webkitwebview.html
import webkit

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
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

        # settings = webkit.WebSettings()
        # settings.set_property ("enable-offline-web-application-cache", "FALSE")
        # self.ctrl.set_settings (settings)

        self.ctrl.connect("navigation-policy-decision-requested", self.__onNavigate)
        self.ctrl.connect("hovering-over-link", self.__onHoveredOverLink)
        #self.ctrl.connect("populate-popup", self._on_populate_popup)

        self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_COPY)
        self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_CUT)

        # self.ctrl.get_settings().set_property("enable-page-cache", False)
        self.ctrl.get_settings().set_property("tab-key-cycles-through-elements", False)
        

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
    #    for i in menu.get_children():
    #        action = i.get_children()[0].get_label()
    #        print i.get_children()[0]["id"]



    def __identifyUri (self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, page, filename)
        """
        basepath = unicode (self.ctrl.get_main_frame().get_uri(), "utf8")
        identifier = UriIdentifierWebKit (self._currentPage, basepath)

        return identifier.identify (href)


    def __onHoveredOverLink (self, view, title, uri):
        if uri == None:
            outwiker.core.commands.setStatusText (u"", self._status_item)
            return

        try:
            href = unicode (urllib.unquote (uri), "utf8")
        except UnicodeDecodeError:
            outwiker.core.commands.setStatusText (u"", self._status_item)
            return

        (url, page, filename, anchor) = self.__identifyUri (href)

        if url != None:
            outwiker.core.commands.setStatusText (url, self._status_item)
            return

        if page != None:
            outwiker.core.commands.setStatusText (page.subpath, self._status_item)
            return

        if filename != None:
            outwiker.core.commands.setStatusText (filename, self._status_item)
            return

        if anchor != None:
            outwiker.core.commands.setStatusText (anchor, self._status_item)
            return

        outwiker.core.commands.setStatusText (u"", self._status_item)


    def __onNavigate (self, view, frame, request, action, decision):
        # Проверка на то, что мы не пытаемся открыть вложенный фрейм
        if frame != self.ctrl.get_main_frame():
            return False

        # Проверка на перезагрузку страницы
        if action.get_reason().value_nick == "reload":
            return True

        curr_href = self.ctrl.get_main_frame().get_uri()

        try:
            href = unicode (urllib.unquote (request.get_uri()), "utf8")
        except UnicodeDecodeError:
            return True

        if self.canOpenUrl or href == curr_href:
            # Если вызов uri осуществляется из программы или это запрос на обновление, то 
            # разрешить обработать запрос компоненту 
            return False
        else:
            button = action.get_button()
            modifier = action.get_modifier_state()
            return self.__onLinkClicked (href, button, modifier)


    def __onLinkClicked (self, href, button, modifier):
        """
        Клик по ссылке
        Возвращает False, если обрабатывать ссылку разрешить компоненту, 
        в противном случае - True
        href - ссылка
        button - кнопка мыши, с помощью которой кликнули по ссылке (1 - левая, 2 - средняя, 3 - правая, -1 - не известно)
        modifier - зажатые клавиши (1 - Shift, 4 - Ctrl)
        """
        middle_button = 2
        ctrl_key = 4

        (url, page, filename, anchor) = self.__identifyUri (href)

        if url != None:
            self.openUrl (url)

        elif page != None and (button == middle_button or modifier == ctrl_key):
            Application.mainWindow.tabsController.openInTab (page, True)

        elif page != None:
            self._currentPage.root.selectedPage = page

        elif filename != None:
            try:
                outwiker.core.system.getOS().startFile (filename)
            except OSError:
                text = _(u"Can't execute file '%s'") % filename
                outwiker.core.commands.MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)

        elif anchor != None:
            return False

        return True

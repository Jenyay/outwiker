import wx

import gobject
gobject.threads_init()

import pygtk
pygtk.require('2.0')
import gtk, gtk.gdk

# pywebkitgtk (http://code.google.com/p/pywebkitgtk/)
import webkit


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

	# Some basic usefull methods
	#def SetEditable(self, editable=True):
	#	self.ctrl.set_editable(editable)

	def LoadPage (self, fname):
		self.ctrl.load_uri("file://{0}".format (fname) )

	#def HistoryBack(self):
	#	self.ctrl.go_back()

	#def HistoryForward(self):
	#	self.ctrl.go_forward()

	#def StopLoading(self):
	#	self.ctrl.stop_loading()

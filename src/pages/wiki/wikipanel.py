#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import os
import hashlib

import core.commands
from core.config import Config, StringOption
from core.tree import RootWikiPage
from core.htmlimprover import HtmlImprover
from core.application import Application
from core.attachment import Attachment

from gui.TextEditor import TextEditor
from gui.BaseTextPanel import BaseTextPanel
from gui.HtmlTextEditor import HtmlTextEditor
from pages.html.HtmlPanel import HtmlPanel
from parserfactory import ParserFactory
from wikiconfig import WikiConfig
from htmlgenerator import HtmlGenerator


class WikiPagePanel (HtmlPanel):
	def __init__ (self, *args, **kwds):
		HtmlPanel.__init__ (self, *args, **kwds)

		self._configSection = u"wiki"
		self._hashKey = u"md5_hash"
		
		self.notebook.SetPageText (0, _(u"Wiki"))

		self.htmlSizer = wx.FlexGridSizer(1, 1, 0, 0)
		self.htmlSizer.AddGrowableRow(0)
		self.htmlSizer.AddGrowableCol(0)

		# Номер вкладки с кодом HTML. -1, если вкладки нет
		self.htmlcodePageIndex = -1

		self.config = WikiConfig (Application.config)

		if self.config.showHtmlCodeOptions.value:
			self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)
		
		self.Layout()


	def __createHtmlCodePanel (self, parentSizer):
		# Окно для просмотра получившегося кода HTML
		self.htmlCodeWindow = HtmlTextEditor(self.notebook, -1)
		self.htmlCodeWindow.SetReadOnly (True)
		parentSizer.Add(self.htmlCodeWindow, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 2)
		
		self.notebook.AddPage (self.htmlCodeWindow, _("HTML"))
		return self.notebook.GetPageCount () - 1
	

	def GetTextEditor(self):
		return TextEditor


	def GetSearchPanel (self):
		if self.notebook.GetSelection() == self.codePageIndex:
			return self.codeEditor.searchPanel
		elif self.notebook.GetSelection() == self.htmlcodePageIndex:
			return self.htmlCodeWindow.searchPanel

		return None
	

	def onTabChanged(self, event): # wxGlade: HtmlPanel.<event_handler>
		if self._currentpage == None:
			return

		if event.GetSelection() == self.codePageIndex:
			self._onSwitchToCode()
		elif event.GetSelection() == self.resultPageIndex:
			self._onSwitchToPreview()
		elif event.GetSelection() == self.htmlcodePageIndex:
			self._onSwitchCodeHtml()


	def _onSwitchCodeHtml (self):
		assert self._currentpage != None

		self.Save()
		core.commands.setStatusText (_(u"Page rendered. Please wait…") )
		Application.onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

		try:
			self.currentHtmlFile = self.generateHtml (self._currentpage)
			self._showHtmlCode(self.currentHtmlFile)
		except IOError as e:
			# TODO: Проверить под Windows
			core.commands.MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
					_(u"Error"), 
					wx.ICON_ERROR | wx.OK)
		except OSError as e:
			core.commands.MessageBox (_(u"Can't save HTML-file\n\n%s") % (unicode (e)), 
					_(u"Error"), 
					wx.ICON_ERROR | wx.OK)

		core.commands.setStatusText (u"")
		Application.onHtmlRenderingEnd (self._currentpage, self.htmlWindow)

		self._enableTools (self.pageToolsMenu, False)
		self.htmlCodeWindow.SetFocus()
		self.htmlCodeWindow.Update()


	def _showHtmlCode (self, path):
		try:
			with open (path) as fp:
				text = unicode (fp.read(), "utf8")

				self.htmlCodeWindow.SetReadOnly (False)
				self.htmlCodeWindow.SetText (text)
				self.htmlCodeWindow.SetReadOnly (True)
		except IOError:
			core.commands.MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		except OSError:
			core.commands.MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)


	def __addFontTools (self):
		"""
		Добавить инструменты, связанные со шрифтами
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_BOLD", 
				lambda event: self.codeEditor.turnText (u"'''", u"'''"), 
				_(u"Bold\tCtrl+B"), 
				_(u"Bold"), 
				os.path.join (self.imagesDir, "text_bold.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_ITALIC", 
				lambda event: self.codeEditor.turnText (u"''", u"''"), 
				_(u"Italic\tCtrl+I"), 
				_(u"Italic"), 
				os.path.join (self.imagesDir, "text_italic.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_BOLD_ITALIC", 
				lambda event: self.codeEditor.turnText (u"''''", u"''''"), 
				_(u"Bold italic\tCtrl+Shift+I"), 
				_(u"Bold italic"), 
				os.path.join (self.imagesDir, "text_bold_italic.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_UNDERLINE", 
				lambda event: self.codeEditor.turnText (u"{+", u"+}"), 
				_(u"Underline\tCtrl+U"), 
				_(u"Underline"), 
				os.path.join (self.imagesDir, "text_underline.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_STRIKE", 
				lambda event: self.codeEditor.turnText (u"{-", u"-}"), 
				_(u"Strikethrough\tCtrl+K"), 
				_(u"Strikethrough"), 
				os.path.join (self.imagesDir, "text_strikethrough.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_SUBSCRIPT", 
				lambda event: self.codeEditor.turnText (u"'_", u"_'"), 
				_(u"Subscript\tCtrl+="), 
				_(u"Subscript"), 
				os.path.join (self.imagesDir, "text_subscript.png"))


		self._addTool (self.pageToolsMenu, 
				"ID_SUPERSCRIPT", 
				lambda event: self.codeEditor.turnText (u"'^", u"^'"), 
				_(u"Superscript\tCtrl++"), 
				_(u"Superscript"), 
				os.path.join (self.imagesDir, "text_superscript.png"))
	

	def __addAlignTools (self):
		self._addTool (self.pageToolsMenu, 
				"ID_ALIGN_CENTER", 
				lambda event: self.codeEditor.turnText (u"%center%", u""), 
				_(u"Center align\tCtrl+Alt+C"), 
				_(u"Center align"), 
				os.path.join (self.imagesDir, "text_align_center.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_ALIGN_RIGHT", 
				lambda event: self.codeEditor.turnText (u"%right%", u""), 
				_(u"Right align\tCtrl+ALT+R"), 
				_(u"Right align"), 
				os.path.join (self.imagesDir, "text_align_right.png"))
	

	def __addFormatTools (self):
		self._addTool (self.pageToolsMenu, 
				"ID_PREFORMAT", 
				lambda event: self.codeEditor.turnText (u"[@", u"@]"), 
				_(u"Preformat [@…@]"), 
				_(u"Preformat [@…@]"), 
				None)

		self._addTool (self.pageToolsMenu, 
				"ID_NONFORMAT", 
				lambda event: self.codeEditor.turnText (u"[=", u"=]"), 
				_(u"Non-parsed [=…=]"), 
				_(u"Non-parsed [=…=]"), 
				None)

	

	def __addTableTools (self):
		"""
		Добавить инструменты, связанные с таблицами
		"""
		#self._addTool (self.pageToolsMenu, 
		#		self.toolsId["ID_TABLE"], 
		#		lambda event: self.codeEditor.turnText (u'<table>', u'</table>'), 
		#		u"Table\tCtrl+Q", 
		#		u"Table (<table>…</table>)", 
		#		os.path.join (self.imagesDir, "table.png"))

		#self._addTool (self.pageToolsMenu, 
		#		self.toolsId["ID_TABLE_TR"], 
		#		lambda event: self.codeEditor.turnText (u'<tr>',u'</tr>'), 
		#		u"Table row\tCtrl+W", 
		#		u"Table row (<tr>…</tr>)", 
		#		os.path.join (self.imagesDir, "table_insert_row.png"))


		#self._addTool (self.pageToolsMenu, 
		#		self.toolsId["ID_TABLE_TD"], 
		#		lambda event: self.codeEditor.turnText (u'<td>', u'</td>'), 
		#		u"Table cell\tCtrl+Y", 
		#		u"Table cell (<td>…</td>)", 
		#		os.path.join (self.imagesDir, "table_insert_cell.png"))

		pass

	
	def __addListTools (self):
		"""
		Добавить инструменты, связанные со списками
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_MARK_LIST", 
				lambda event: self.codeEditor.turnList (u'', u'', u'*', u''), 
				_(u"Bullets list\tCtrl+G"), 
				_(u"Bullets list"), 
				os.path.join (self.imagesDir, "text_list_bullets.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_NUMBER_LIST", 
				lambda event: self.codeEditor.turnList (u'', u'', u'#', u''), 
				_(u"Numbers list\tCtrl+J"), 
				_(u"Numbers list"), 
				os.path.join (self.imagesDir, "text_list_numbers.png"))
	

	def __addHTools (self):
		"""
		Добавить инструменты для заголовочных тегов <H>
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_H1", 
				lambda event: self.codeEditor.turnText (u"\n!! ", u""), 
				_(u"H1\tCtrl+1"), 
				_(u"H1"), 
				os.path.join (self.imagesDir, "text_heading_1.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H2", 
				lambda event: self.codeEditor.turnText (u"!!! ", u""), 
				_(u"H2\tCtrl+2"), 
				_(u"H2"), 
				os.path.join (self.imagesDir, "text_heading_2.png"))
		
		self._addTool (self.pageToolsMenu, 
				"ID_H3", 
				lambda event: self.codeEditor.turnText (u"!!!! ", u""), 
				_(u"H3\tCtrl+3"), 
				_(u"H3"), 
				os.path.join (self.imagesDir, "text_heading_3.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H4", 
				lambda event: self.codeEditor.turnText (u"!!!!! ", u""), 
				_(u"H4\tCtrl+4"), 
				_(u"H4"), 
				os.path.join (self.imagesDir, "text_heading_4.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H5", 
				lambda event: self.codeEditor.turnText (u"!!!!!! ", u""), 
				_(u"H5\tCtrl+5"), 
				_(u"H5"), 
				os.path.join (self.imagesDir, "text_heading_5.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H6", 
				lambda event: self.codeEditor.turnText (u"!!!!!!! ", u""), 
				_(u"H6\tCtrl+6"), 
				_(u"H6"), 
				os.path.join (self.imagesDir, "text_heading_6.png"))
	

	def __addOtherTools (self):
		"""
		Добавить остальные инструменты
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_THUMB", 
				lambda event: self.codeEditor.turnText (u'%thumb%', u'%%'), 
				_(u'Thumbnail\tCtrl+M'), 
				_(u'Thumbnail'), 
				os.path.join (self.imagesDir, "images.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_LINK", 
				lambda event: self.codeEditor.turnText (u'[[', u']]'), 
				_(u"Link\tCtrl+L"), 
				_(u'Link'), 
				os.path.join (self.imagesDir, "link.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_HORLINE", 
				lambda event: self.codeEditor.replaceText (u'----'), 
				_(u"Horizontal line\tCtrl+H"), 
				_(u"Horizontal line"), 
				os.path.join (self.imagesDir, "text_horizontalrule.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_EQUATION", 
				lambda event: self.codeEditor.turnText (u'{$', u'$}'), 
				_(u"Equation\tCtrl+Q"), 
				_(u'Equation'), 
				os.path.join (self.imagesDir, "equation.png"))

		self.pageToolsMenu.AppendSeparator()

		self._addTool (self.pageToolsMenu, 
				"ID_ESCAPEHTML", 
				self.codeEditor.escapeHtml, 
				_(u"Convert HTML Symbols"), 
				_(u"Convert HTML Symbols"), 
				None)

	
	def initGui (self, mainWindow):
		if not self._guiInitialized:
			BaseTextPanel.initGui (self, mainWindow)

			self.pageToolsMenu = wx.Menu()

			self._addTool (self.pageToolsMenu, 
					"ID_HTMLCODE", 
					self.__openHtmlCode, 
					_(u"HTML Code\tShift+F4"), 
					_(u"HTML Code"), 
					os.path.join (self.imagesDir, "html.png"),
					True)

			self._addRenderTools()
			self.__addCommandsTools()
			self.__addFontTools()
			self.__addAlignTools()
			self.__addHTools()
			self.__addTableTools()
			self.__addListTools()
			self.__addFormatTools()
			self.__addOtherTools()

			mainWindow.mainMenu.Insert (mainWindow.mainMenu.GetMenuCount() - 1, 
					self.pageToolsMenu, 
					_(u"&Wiki") )

			mainWindow.mainToolbar.Realize()

		self._openDefaultPage()


	def __addCommandsTools (self):
		self.commandsMenu = wx.Menu()
		self.pageToolsMenu.AppendSubMenu (self.commandsMenu, _(u"Commands"))

		self._addTool (self.commandsMenu, 
				"ID_LJUSER", 
				lambda event: self.codeEditor.turnText (u"(:ljuser ", u":)"), 
				_(u"Livejournal User (:ljuser ...:)"), 
				_(u"Livejournal User (:ljuser ...:)"), 
				None)

		self._addTool (self.commandsMenu, 
				"ID_LJCOMM", 
				lambda event: self.codeEditor.turnText (u"(:ljcomm ", u":)"), 
				_(u"Livejournal Community (:ljcomm ...:)"), 
				_(u"Livejournal Community (:ljcomm ...:)"), 
				None)


		self._addTool (self.commandsMenu, 
				"ID_ATTACHLIST", 
				lambda event: self.codeEditor.replaceText (u"(:attachlist:)"), 
				_(u"Attachment (:attachlist:)"), 
				_(u"Attachment (:attachlist:)"), 
				None)

		self._addTool (self.commandsMenu, 
				"ID_CHILDLIST", 
				lambda event: self.codeEditor.replaceText (u"(:childlist:)"), 
				_(u"Children (:childlist:)"), 
				_(u"Children (:childlist:)"), 
				None)


		self._addTool (self.commandsMenu, 
				"ID_INCLUDE", 
				lambda event: self.codeEditor.turnText (u"(:include ", u":)"), 
				_(u"Include (:include ...:)"), 
				_(u"Include (:include ...:)"), 
				None)


	def __openHtmlCode (self, event):
		if self.htmlcodePageIndex == -1:
			self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

		self.notebook.SetSelection (self.htmlcodePageIndex)

	
	def generateHtml (self, page):
		generator = HtmlGenerator (page)
		return generator.makeHtml()


	def removeGui (self):
		HtmlPanel.removeGui (self)
		self.mainWindow.mainMenu.Remove (self.mainWindow.mainMenu.GetMenuCount() - 2)

	
	def _getAttachString (self, fnames):
		"""
		Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений

		Перегрузка метода из BaseTextPanel
		"""
		text = ""
		count = len (fnames)

		for n in range (count):
			text += "Attach:" + fnames[n]
			if n != count -1:
				text += "\n"

		return text

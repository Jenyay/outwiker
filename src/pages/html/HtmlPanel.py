# -*- coding: utf-8 -*-

import os
import re
from abc import ABCMeta, abstractmethod
import cgi

import wx

import core.system
import core.commands
from core.application import Application
from core.attachment import Attachment
from core.htmlimprover import HtmlImprover
from core.htmltemplate import HtmlTemplate

from gui.BaseTextPanel import BaseTextPanel
from gui.htmlrenderfactory import getHtmlRender
from gui.HtmlTextEditor import HtmlTextEditor
from core.system import getTemplatesDir


class ToolsInfo (object):
	def __init__ (self, id, alwaysEnabled):
		"""
		id - идентификатор
		alwaysEnabled - кнопка всегда активна?
		"""
		self.id = id
		self.alwaysEnabled = alwaysEnabled


class HtmlPanel(BaseTextPanel):
	__metaclass__ = ABCMeta
	
	def __init__(self, parent, *args, **kwds):
		BaseTextPanel.__init__ (self, parent, *args, **kwds)

		self._htmlFile = "__content.html"
		self.currentHtmlFile = None

		# Номера страниц-вкладок
		self.codePageIndex = 0
		self.resultPageIndex = 1

		self.imagesDir = core.system.getImagesDir()

		self.notebook = wx.Notebook(self, -1, style=wx.NB_BOTTOM)
		self.codeEditor = self.GetTextEditor()(self.notebook)
		self.htmlWindow = getHtmlRender (self.notebook)

		self.__do_layout()

		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChanged, self.notebook)

		self.toolsId = {}


	def Print (self):
		currpanel = self.notebook.GetCurrentPage()
		if currpanel != None:
			currpanel.Print()


	def GetTextEditor(self):
		return HtmlTextEditor

	
	def onEditorConfigChange (self):
		self.codeEditor.setDefaultSettings()

	
	def onClose (self, event):
		self.htmlWindow.Close()
		pass


	def onAttachmentPaste (self, fnames):
		text = self._getAttachString (fnames)
		self.codeEditor.AddText (text)
		self.codeEditor.SetFocus()

	
	def UpdateView (self, page):
		self.htmlWindow.page = self._currentpage

		self.codeEditor.SetReadOnly (False)
		self.codeEditor.SetText (self._currentpage.content)
		self.codeEditor.EmptyUndoBuffer()
		self.codeEditor.SetReadOnly (page.readonly)

		self._showHtml()
		self._openDefaultPage()


	def GetContentFromGui(self):
		return self.codeEditor.GetText()
	
	
	def __do_layout(self):
		grid_sizer_7 = wx.FlexGridSizer(1, 1, 0, 0)
		grid_sizer_9 = wx.FlexGridSizer(1, 1, 0, 0)
		grid_sizer_9.Add(self.htmlWindow, 1, wx.EXPAND, 0)
		grid_sizer_9.AddGrowableRow(0)
		grid_sizer_9.AddGrowableCol(0)
		self.notebook.AddPage(self.codeEditor, _("HTML"))
		self.notebook.AddPage(self.htmlWindow, _("Preview"))
		grid_sizer_7.Add(self.notebook, 1, wx.EXPAND, 0)
		grid_sizer_7.Fit(self)
		grid_sizer_7.AddGrowableRow(0)
		grid_sizer_7.AddGrowableCol(0)

		self.SetSizer(grid_sizer_7)

		self.Bind (wx.EVT_CLOSE, self.onClose)


	@abstractmethod
	def generateHtml (self, page):
		pass


	def getHtmlPath (self, path):
		"""
		Получить путь до результирующего файла HTML
		"""
		path = os.path.join (self._currentpage.path, self._htmlFile)
		return path


	def removeHtml (self):
		"""
		Удалить сгенерированный HTML-файл
		"""
		if self.currentHtmlFile != None:
			try:
				os.remove (self.currentHtmlFile)
			except OSError:
				pass
	

	def _openDefaultPage(self):
		assert self._currentpage != None

		if len (self._currentpage.content) > 0 or len (Attachment (self._currentpage).attachmentFull) > 0:
			self.notebook.SetSelection (self.resultPageIndex)
		else:
			self.notebook.SetSelection (self.codePageIndex)
			self.codeEditor.SetFocus()


	def onTabChanged(self, event):
		if self._currentpage == None:
			return

		if event.GetSelection() == self.resultPageIndex:
			self._onSwitchToPreview()
		else:
			self._onSwitchToCode()
	

	def _onSwitchToCode (self):
		"""
		Обработка события при переключении на код страницы
		"""
		self._enableTools (self.pageToolsMenu, True)
		self.codeEditor.SetFocus()

	
	def _onSwitchToPreview (self):
		"""
		Обработка события при переключении на просмотр страницы
		"""
		self.Save()
		self._enableTools (self.pageToolsMenu, False)
		self.htmlWindow.SetFocus()
		self.htmlWindow.Update()
		self._showHtml()
	

	def _showHtml (self):
		"""
		Подготовить и показать HTML текущей страницы
		"""
		assert self._currentpage != None

		core.commands.setStatusText (_(u"Page rendered. Please wait…") )
		Application.onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

		try:
			self.currentHtmlFile = self.generateHtml (self._currentpage)
			self.htmlWindow.LoadPage (self.currentHtmlFile)
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
	

	def _enableTools (self, menu, enable):
		for key in self.toolsId:
			if not self.toolsId[key].alwaysEnabled:
				if self.mainWindow.mainToolbar.FindById (self.toolsId[key].id) != None:
					self.mainWindow.mainToolbar.EnableTool (self.toolsId[key].id, enable)
				menu.Enable (self.toolsId[key].id, enable)
	

	def GetSearchPanel (self):
		if self.notebook.GetSelection() == self.codePageIndex:
			return self.codeEditor.searchPanel

		return None


	def _removeTool (self, id):
		if self.mainWindow.mainToolbar.FindById (id) != None:
			self.mainWindow.mainToolbar.DeleteTool (id)
		self.mainWindow.Unbind(wx.EVT_MENU, id=id)


	def _addRenderTools (self):
		self._addTool (self.pageToolsMenu, 
				"ID_RENDER", 
				self.__switchView, 
				_(u"Code / Preview\tF4"), 
				_(u"Code / Preview"), 
				os.path.join (self.imagesDir, "render.png"),
				True)

		self.pageToolsMenu.AppendSeparator()


	def __switchView (self, event):
		if self._currentpage == None:
			return

		if self.notebook.GetSelection() == self.codePageIndex:
			self.notebook.SetSelection (self.resultPageIndex)
		else:
			self.notebook.SetSelection (self.codePageIndex)


	def _addTool (self, menu, idstring, func, menuText, buttonText, image, alwaysEnabled = False):
		"""
		Добавить пункт меню и кнопку на панель
		menu -- меню для добавления элемента
		id -- идентификатор меню и кнопки
		func -- обработчик
		menuText -- название пунта меню
		buttonText -- подсказка для кнопки
		image -- имя файла с картинкой
		disableOnView -- дизаблить кнопку при переключении на просмотр результата
		"""
		id = wx.NewId()
		self.toolsId[idstring] = ToolsInfo (id, alwaysEnabled)

		menu.Append (id, menuText, "", wx.ITEM_NORMAL)
		self.mainWindow.Bind(wx.EVT_MENU, func, id = id)

		if image != None and len (image) != 0:
			self.mainWindow.mainToolbar.AddLabelTool(id, 
					buttonText, 
					wx.Bitmap(image, wx.BITMAP_TYPE_ANY), 
					wx.NullBitmap, 
					wx.ITEM_NORMAL, 
					buttonText, 
					"")
	

	def removeGui (self):
		BaseTextPanel.removeGui (self)

		for key in self.toolsId.keys ():
			self._removeTool (self.toolsId[key].id)


	


# end of class HtmlPanel

class HtmlPagePanel (HtmlPanel):
	def __init__ (self, parent, *args, **kwds):
		HtmlPanel.__init__ (self, parent, *args, **kwds)
		self.__createCustomTools()


	def __createCustomTools (self):
		"""
		Создать кнопки и меню для данного типа страниц
		"""
		assert self.mainWindow != None

		self.pageToolsMenu = wx.Menu()
		
		self._addRenderTools()
		self.__addFontTools()
		self.__addAlignTools()
		self.__addHTools()
		self.__addTableTools()
		self.__addListTools()
		self.__addOtherTools()

		self.mainWindow.mainMenu.Insert (self.mainWindow.mainMenu.GetMenuCount() - 1, self.pageToolsMenu, _(u"H&tml"))
		self.mainWindow.mainToolbar.Realize()


	def __addFontTools (self):
		"""
		Добавить инструменты, связанные со шрифтами
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_BOLD", 
				lambda event: self.codeEditor.turnText (u"<b>", u"</b>"), 
				_(u"Bold\tCtrl+B"), 
				_(u"Bold (<b>…</b>)"), 
				os.path.join (self.imagesDir, "text_bold.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_ITALIC", 
				lambda event: self.codeEditor.turnText (u"<i>", u"</i>"), 
				_(u"Italic\tCtrl+I"), 
				_(u"Italic (<i>…</i>)"), 
				os.path.join (self.imagesDir, "text_italic.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_UNDERLINE", 
				lambda event: self.codeEditor.turnText (u"<u>", u"</u>"), 
				_(u"Underline\tCtrl+U"), 
				_(u"Underline (<u>…</u>)"), 
				os.path.join (self.imagesDir, "text_underline.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_STRIKE", 
				lambda event: self.codeEditor.turnText (u"<strike>", u"</strike>"), 
				_(u"Strikethrough\tCtrl+K"), 
				_(u"Strikethrough (<strike>…</strike>)"), 
				os.path.join (self.imagesDir, "text_strikethrough.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_SUBSCRIPT", 
				lambda event: self.codeEditor.turnText (u"<sub>", u"</sub>"), 
				_(u"Subscript\tCtrl+="), 
				_(u"Subscript (<sub>…</sub>)"), 
				os.path.join (self.imagesDir, "text_subscript.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_SUPERSCRIPT", 
				lambda event: self.codeEditor.turnText (u"<sup>", u"</sup>"), 
				_(u"Superscript\tCtrl++"), 
				_(u"Superscript (<sup>…</sup>)"), 
				os.path.join (self.imagesDir, "text_superscript.png"))

	
	def __addAlignTools (self):
		self._addTool (self.pageToolsMenu, 
				"ID_ALIGN_CENTER", 
				lambda event: self.codeEditor.turnText (u'<div align="center">', u'</div>'), 
				_(u"Center align\tCtrl+Alt+C"), 
				_(u"Center align"), 
				os.path.join (self.imagesDir, "text_align_center.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_ALIGN_RIGHT", 
				lambda event: self.codeEditor.turnText (u'<div align="right">', u'</div>'), 
				_(u"Right align\tCtrl+Alt+R"), 
				_(u"Right align"), 
				os.path.join (self.imagesDir, "text_align_right.png"))
	

	def __addTableTools (self):
		"""
		Добавить инструменты, связанные с таблицами
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_TABLE", 
				lambda event: self.codeEditor.turnText (u'<table>', u'</table>'), 
				_(u"Table\tCtrl+Q"), 
				_(u"Table (<table>…</table>)"), 
				os.path.join (self.imagesDir, "table.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_TABLE_TR", 
				lambda event: self.codeEditor.turnText (u'<tr>',u'</tr>'), 
				_(u"Table row\tCtrl+W"), 
				_(u"Table row (<tr>…</tr>)"), 
				os.path.join (self.imagesDir, "table_insert_row.png"))


		self._addTool (self.pageToolsMenu, 
				"ID_TABLE_TD", 
				lambda event: self.codeEditor.turnText (u'<td>', u'</td>'), 
				_(u"Table cell\tCtrl+Y"), 
				_(u"Table cell (<td>…</td>)"), 
				os.path.join (self.imagesDir, "table_insert_cell.png"))

	
	def __addListTools (self):
		"""
		Добавить инструменты, связанные со списками
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_MARK_LIST", 
				lambda event: self.codeEditor.turnList (u'<ul>\n', u'</ul>', u'<li>', u'</li>'), 
				_(u"Bullets list\tCtrl+G"), 
				_(u"Bullets list (<ul>…</ul>)"), 
				os.path.join (self.imagesDir, "text_list_bullets.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_NUMBER_LIST", 
				lambda event: self.codeEditor.turnList (u'<ol>\n', u'</ol>', u'<li>', u'</li>'), 
				_(u"Numbers list\tCtrl+J"), 
				_(u"Numbers list (<ul>…</ul>)"), 
				os.path.join (self.imagesDir, "text_list_numbers.png"))
	

	def __addHTools (self):
		"""
		Добавить инструменты для заголовочных тегов <H>
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_H1", 
				lambda event: self.codeEditor.turnText (u"<h1>", u"</h1>"), 
				_(u"H1\tCtrl+1"), 
				_(u"H1 (<h1>…</h1>)"), 
				os.path.join (self.imagesDir, "text_heading_1.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H2", 
				lambda event: self.codeEditor.turnText (u"<h2>", u"</h2>"), 
				_(u"H2\tCtrl+2"), 
				_(u"H2 (<h2>…</h2>)"), 
				os.path.join (self.imagesDir, "text_heading_2.png"))
		
		self._addTool (self.pageToolsMenu, 
				"ID_H3", 
				lambda event: self.codeEditor.turnText (u"<h3>", u"</h3>"), 
				_(u"H3\tCtrl+3"), 
				_(u"H3 (<h3>…</h3>)"), 
				os.path.join (self.imagesDir, "text_heading_3.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H4", 
				lambda event: self.codeEditor.turnText (u"<h4>", u"</h4>"), 
				_(u"H4\tCtrl+4"), 
				_(u"H4 (<h4>…</h4>)"), 
				os.path.join (self.imagesDir, "text_heading_4.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H5", 
				lambda event: self.codeEditor.turnText (u"<h5>", u"</h5>"), 
				_(u"H5\tCtrl+5"), 
				_(u"H5 (<h5>…</h5>)"), 
				os.path.join (self.imagesDir, "text_heading_5.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H6", 
				lambda event: self.codeEditor.turnText (u"<h6>", u"</h6>"), 
				_(u"H6\tCtrl+6"), 
				_(u"H6 (<h6>…</h6>)"), 
				os.path.join (self.imagesDir, "text_heading_6.png"))
	

	def __addOtherTools (self):
		"""
		Добавить остальные инструменты
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_IMAGE", 
				lambda event: self.codeEditor.turnText (u'<img src="', u'"/>'), 
				_(u'Image\tCtrl+M'), 
				_(u'Image (<img src="…"/>'), 
				os.path.join (self.imagesDir, "image.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_LINK", 
				lambda event: self.codeEditor.turnText (u'<a href="">', u'</a>'), 
				_(u"Link\tCtrl+L"), 
				_(u'Link (<a href="…">…</a>)'), 
				os.path.join (self.imagesDir, "link.png"))


		self._addTool (self.pageToolsMenu, 
				"ID_ANCHOR", 
				lambda event: self.codeEditor.turnText (u'<a name="', u'"></a>'), 
				_(u"Anchor\tCtrl+Alt+L"), 
				_(u'Anchor (<a name="…">…</a>)'), 
				os.path.join (self.imagesDir, "anchor.png"))


		self._addTool (self.pageToolsMenu, 
				"ID_HORLINE", 
				lambda event: self.codeEditor.replaceText (u'<hr>'), 
				_(u"Horizontal line\tCtrl+H"), 
				_(u"Horizontal line (<hr>)"), 
				os.path.join (self.imagesDir, "text_horizontalrule.png"))


		self._addTool (self.pageToolsMenu, 
				"ID_CODE", 
				lambda event: self.codeEditor.turnText (u"<code>", u"</code>"), 
				_(u"Code\tCtrl+Alt+D"), 
				_(u"Code (<code>…</code>)"), 
				os.path.join (self.imagesDir, "code.png"))


		self._addTool (self.pageToolsMenu, 
				"ID_PREFORMAT", 
				lambda event: self.codeEditor.turnText (u"<pre>", u"</pre>"), 
				_(u"Preformat\tCtrl+Alt+F"), 
				_(u"Preformat (<pre>…</pre>)"), 
				None)


		self._addTool (self.pageToolsMenu, 
				"ID_BLOCKQUOTE", 
				lambda event: self.codeEditor.turnText (u"<blockquote>", u"</blockquote>"), 
				_(u"Quote\tCtrl+Alt+Q"), 
				_(u"Quote (<blockquote>…</blockquote>)"), 
				os.path.join (self.imagesDir, "quote.png"))


		self.pageToolsMenu.AppendSeparator()

		self._addTool (self.pageToolsMenu, 
				"ID_ESCAPEHTML", 
				self.codeEditor.escapeHtml, 
				_(u"Convert HTML Symbols"), 
				_(u"Convert HTML Symbols"), 
				None)


	def generateHtml (self, page):
		path = self.getHtmlPath (page)

		if page.readonly and os.path.exists (path):
			# Если страница открыта только для чтения и html-файл уже существует, то покажем его
			return path

		tpl = HtmlTemplate (os.path.join (getTemplatesDir(), "html") )
		text = HtmlImprover.run (page.content)
		text = re.sub ("\n<BR>\n(<li>)|(<LI>)", "\n<LI>", text)

		result = tpl.substitute (content=text)

		with open (path, "wb") as fp:
			fp.write (result.encode ("utf-8"))

		return path


	def removeGui (self):
		HtmlPanel.removeGui (self)
		self.mainWindow.mainMenu.Remove (self.mainWindow.mainMenu.GetMenuCount() - 2)

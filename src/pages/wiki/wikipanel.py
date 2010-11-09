#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import os
import hashlib

from pages.html.HtmlPanel import HtmlPanel
from gui.BaseTextPanel import BaseTextPanel
from wikiparser import Parser
from core.config import Config
from core.tree import RootWikiPage
from pages.wiki.htmlimprover import HtmlImprover

class WikiPagePanel (HtmlPanel):
	def __init__ (self, *args, **kwds):
		HtmlPanel.__init__ (self, *args, **kwds)

		self._configSection = u"wiki"
		self._hashKey = u"md5_hash"

		self.HtmlView.SetPageText (0, _(u"Wiki"))


	def __addFontTools (self):
		"""
		Добавить инструменты, связанные со шрифтами
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_BOLD", 
				lambda event: self._turnText (u"'''", u"'''"), 
				_(u"Bold\tCtrl+B"), 
				_(u"Bold"), 
				os.path.join (self.imagesDir, "text_bold.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_ITALIC", 
				lambda event: self._turnText (u"''", u"''"), 
				_(u"Italic\tCtrl+I"), 
				_(u"Italic"), 
				os.path.join (self.imagesDir, "text_italic.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_BOLD_ITALIC", 
				lambda event: self._turnText (u"''''", u"''''"), 
				_(u"Bold italic\tCtrl+Shift+I"), 
				_(u"Bold italic"), 
				os.path.join (self.imagesDir, "text_bold_italic.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_UNDERLINE", 
				lambda event: self._turnText (u"{+", u"+}"), 
				_(u"Underline\tCtrl+U"), 
				_(u"Underline"), 
				os.path.join (self.imagesDir, "text_underline.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_SUBSCRIPT", 
				lambda event: self._turnText (u"'_", u"_'"), 
				_(u"Subscript\tCtrl+="), 
				_(u"Subscript"), 
				os.path.join (self.imagesDir, "text_subscript.png"))


		self._addTool (self.pageToolsMenu, 
				"ID_SUPERSCRIPT", 
				lambda event: self._turnText (u"'^", u"^'"), 
				_(u"Superscript\tCtrl++"), 
				_(u"Superscript"), 
				os.path.join (self.imagesDir, "text_superscript.png"))
	

	def __addAlignTools (self):
		self._addTool (self.pageToolsMenu, 
				"ID_ALIGN_CENTER", 
				lambda event: self._turnText (u"%center%", u""), 
				_(u"Center align\tCtrl+Alt+C"), 
				_(u"Center align"), 
				os.path.join (self.imagesDir, "text_align_center.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_ALIGN_RIGHT", 
				lambda event: self._turnText (u"%right%", u""), 
				_(u"Right align\tCtrl+ALT+R"), 
				_(u"Right align"), 
				os.path.join (self.imagesDir, "text_align_right.png"))
	

	def __addTableTools (self):
		"""
		Добавить инструменты, связанные с таблицами
		"""
		#self._addTool (self.pageToolsMenu, 
		#		self.toolsId["ID_TABLE"], 
		#		lambda event: self._turnText (u'<table>', u'</table>'), 
		#		u"Table\tCtrl+Q", 
		#		u"Table (<table>...</table>)", 
		#		os.path.join (self.imagesDir, "table.png"))

		#self._addTool (self.pageToolsMenu, 
		#		self.toolsId["ID_TABLE_TR"], 
		#		lambda event: self._turnText (u'<tr>',u'</tr>'), 
		#		u"Table row\tCtrl+W", 
		#		u"Table row (<tr>...</tr>)", 
		#		os.path.join (self.imagesDir, "table_insert_row.png"))


		#self._addTool (self.pageToolsMenu, 
		#		self.toolsId["ID_TABLE_TD"], 
		#		lambda event: self._turnText (u'<td>', u'</td>'), 
		#		u"Table cell\tCtrl+Y", 
		#		u"Table cell (<td>...</td>)", 
		#		os.path.join (self.imagesDir, "table_insert_cell.png"))

		pass

	
	def __addListTools (self):
		"""
		Добавить инструменты, связанные со списками
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_MARK_LIST", 
				lambda event: self._turnList (u'', u'', u'*', u''), 
				_(u"Bullets list\tCtrl+G"), 
				_(u"Bullets list"), 
				os.path.join (self.imagesDir, "text_list_bullets.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_NUMBER_LIST", 
				lambda event: self._turnList (u'', u'', u'#', u''), 
				_(u"Numbers list\tCtrl+J"), 
				_(u"Numbers list"), 
				os.path.join (self.imagesDir, "text_list_numbers.png"))
	

	def __addHTools (self):
		"""
		Добавить инструменты для заголовочных тегов <H>
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_H1", 
				lambda event: self._turnText (u"\n!! ", u""), 
				_(u"H1\tCtrl+1"), 
				_(u"H1"), 
				os.path.join (self.imagesDir, "text_heading_1.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H2", 
				lambda event: self._turnText (u"!!! ", u""), 
				_(u"H2\tCtrl+2"), 
				_(u"H2"), 
				os.path.join (self.imagesDir, "text_heading_2.png"))
		
		self._addTool (self.pageToolsMenu, 
				"ID_H3", 
				lambda event: self._turnText (u"!!!! ", u""), 
				_(u"H3\tCtrl+3"), 
				_(u"H3"), 
				os.path.join (self.imagesDir, "text_heading_3.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H4", 
				lambda event: self._turnText (u"!!!!! ", u""), 
				_(u"H4\tCtrl+4"), 
				_(u"H4"), 
				os.path.join (self.imagesDir, "text_heading_4.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H5", 
				lambda event: self._turnText (u"!!!!!! ", u""), 
				_(u"H5\tCtrl+5"), 
				_(u"H5"), 
				os.path.join (self.imagesDir, "text_heading_5.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H6", 
				lambda event: self._turnText (u"!!!!!!! ", u""), 
				_(u"H6\tCtrl+6"), 
				_(u"H6"), 
				os.path.join (self.imagesDir, "text_heading_6.png"))
	

	def __addOtherTools (self):
		"""
		Добавить остальные инструменты
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_THUMB", 
				lambda event: self._turnText (u'%thumb%', u'%%'), 
				_(u'Thumbnail\tCtrl+M'), 
				_(u'Thumbnail'), 
				os.path.join (self.imagesDir, "images.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_LINK", 
				lambda event: self._turnText (u'[[', u']]'), 
				_(u"Link\tCtrl+L"), 
				u'Link', 
				os.path.join (self.imagesDir, "link.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_HORLINE", 
				lambda event: self._replaceText (u'----'), 
				_(u"Horizontal line\tCtrl+H"), 
				_(u"Horizontal line"), 
				os.path.join (self.imagesDir, "text_horizontalrule.png"))

	
	def initGui (self, mainWindow):
		BaseTextPanel.initGui (self, mainWindow)

		self.pageToolsMenu = wx.Menu()

		self._addRenderTools()
		self.__addFontTools()
		self.__addAlignTools()
		self.__addHTools()
		self.__addTableTools()
		self.__addListTools()
		self.__addOtherTools()

		mainWindow.mainMenu.Insert (mainWindow.mainMenu.GetMenuCount() - 1, self.pageToolsMenu, _(u"&Wiki") )
		mainWindow.mainToolbar.Realize()
		self.HtmlView.SetSelection (1)

	
	def _getOldHash (self, page):
		try:
			config = Config (os.path.join (page.path, RootWikiPage.pageConfig))
			old_hash = config.get (self._configSection, self._hashKey)
		except:
			old_hash = ""

		return old_hash


	def _saveHash (self, page, hash):
		#print hash

		try:
			config = Config (os.path.join (page.path, RootWikiPage.pageConfig))
			config.set (self._configSection, self._hashKey, hash)
		except Exception as e:
			wx.MessageBox (_(u"Can't save page hash\n") + str(e), _(u"Error"), wx.OK  | wx.ICON_ERROR)


	def __getFullContent (self, page):
		result = page.content.encode ("unicode_escape")
		for fname in page.attachment:
			result += fname.encode ("unicode_escape")
			result += unicode (os.stat (fname).st_mtime)
		return result

	
	def generateHtml (self, page, path):
		hash = hashlib.md5(self.__getFullContent (page) ).hexdigest()
		old_hash = self._getOldHash(page)

		if os.path.exists (path) and (hash == old_hash or page.readonly):
			return path

		parser = Parser (page)

		text = HtmlImprover.run (parser.toCompleteHtml (page.content) )

		with open (path, "wb") as fp:
			fp.write (text.encode ("utf-8"))

		self._saveHash (page, hash)

		return path


	def removeGui (self):
		HtmlPanel.removeGui (self)
		self.mainWindow.mainMenu.Remove (self.mainWindow.mainMenu.GetMenuCount() - 2)

	
	def _getAttachString (self, fnames):
		text = ""
		count = len (fnames)

		for n in range (count):
			text += "Attach:" + fnames[n]
			if n != count -1:
				text += "\n"

		return text

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import wx

from core.application import Application
from core.factoryselector import FactorySelector
import core.commands
from core.tree import RootWikiPage
from core.search import TagsList
import core.system


class CurrentPagePanel(wx.Panel):
	def __init__(self, *args, **kwds):
		self.pageView = None

		self.imagesDir = core.system.getImagesDir()
		
		self.grayStarImage = os.path.join (self.imagesDir, "star_gray.png")
		self.goldStarImage = os.path.join (self.imagesDir, "star.png")

		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.bookmarkButton = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join (self.imagesDir, "star_gray.png"), wx.BITMAP_TYPE_ANY))
		self.titleLabel = wx.StaticText(self, -1, "")
		self.tagsLabel = wx.StaticText(self, -1, _("[]"))

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.__onBookmark, self.bookmarkButton)

		Application.onWikiOpen += self.__onWikiOpen
		Application.onPageSelect += self.__onPageSelect
		Application.onPageRename += self.__onPageRename
		Application.onPageUpdate += self.__onPageUpdate
		Application.onBookmarksChanged += self.__onBookmarksChanged

		self.Bind (wx.EVT_CLOSE, self.__onClose)


	def Print (self):
		if Application.selectedPage != None and self.pageView != None:
			self.pageView.Print()

	
	def __onClose (self, event):
		Application.onWikiOpen -= self.__onWikiOpen
		Application.onPageSelect -= self.__onPageSelect
		Application.onPageRename -= self.__onPageRename
		Application.onPageUpdate -= self.__onPageUpdate
		Application.onBookmarksChanged -= self.__onBookmarksChanged

		if self.pageView != None:
			self.pageView.removeGui ()
			self.pageView.Close()
		self.Destroy()


	def __onPageRename (self, page, oldsubpath):
		self.__onPageUpdate (page)


	def __onWikiOpen (self, root):
		self.__onPageSelect (root.selectedPage if root != None else None)


	def __onPageSelect (self, page):
		"""
		Событие при выборе страницы
		"""
		self.Freeze()
		self.destroyPageView()

		self.__updatePageInfo (page)
		self.__updatePageView (page)
		self.Thaw()


	def __onPageUpdate (self, page):
		if Application.selectedPage != None and Application.selectedPage == page:
			self.__updatePageInfo (page)
	

	def __updateBookmarkBtn (self):
		imagePath = self.grayStarImage
		tooltip = _(u"Add to Bookmarks")

		if Application.selectedPage != None and Application.selectedPage.root.bookmarks.pageMarked (Application.selectedPage):
			imagePath = self.goldStarImage
			tooltip = _(u"Remove from Bookmarks")

		self.bookmarkButton.SetBitmapLabel (wx.Bitmap(imagePath, wx.BITMAP_TYPE_ANY))
		self.bookmarkButton.SetToolTipString (tooltip)


	def __onBookmarksChanged (self, bookmarks):
		self.__updateBookmarkBtn()


	def __updatePageView (self, page):
		"""
		Обновить вид страницы
		"""
		if page != None:
			factory = FactorySelector.getFactory (page.getTypeString())
			self.pageView = factory.getPageView (page, self)

			assert self.pageView != None

			self.contentSizer.Add (self.pageView, 1, wx.EXPAND, 0)
			#self.contentSizer.Layout()
			self.Layout()

			self.pageView.initGui(Application.mainWindow)


	def __updatePageInfo (self, page):
		"""
		Обновить информацию о странице
		"""
		if page != None:
			title = "%s" % (page.title)
			self.titleLabel.SetLabel (title)

			if hasattr (page, "tags"):
				tags = u"[%s]" % TagsList.getTagsString (page.tags)
			else:
				tags = u"[]"

			self.tagsLabel.SetLabel (tags)

			self.__updateBookmarkBtn()
		else:
			self.titleLabel.SetLabel (u"")
			self.tagsLabel.SetLabel (u"[]")

	
	def __set_properties(self):
		self.bookmarkButton.SetSize(self.bookmarkButton.GetBestSize())
		self.titleLabel.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
		self.tagsLabel.SetFont(wx.Font(12, wx.MODERN, wx.ITALIC, wx.NORMAL, 0, ""))


	def __do_layout(self):
		mainSizer = wx.FlexGridSizer(3, 1, 0, 0)
		contentSizer = wx.FlexGridSizer(1, 1, 0, 0)
		titleSizer = wx.FlexGridSizer(1, 3, 0, 0)
		titleSizer.Add(self.bookmarkButton, 0, 0, 0)
		titleSizer.Add(self.titleLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
		titleSizer.Add(self.tagsLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
		titleSizer.AddGrowableCol(1)
		mainSizer.Add(titleSizer, 1, wx.EXPAND, 0)
		contentSizer.AddGrowableRow(0)
		contentSizer.AddGrowableCol(0)
		mainSizer.Add(contentSizer, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableRow(1)
		mainSizer.AddGrowableCol(0)

		self.contentSizer = contentSizer


	def destroyPageView (self):
		"""
		Уничтожить текущий контрол
		"""
		if self.pageView != None:
			self.contentSizer.Detach (self.pageView)
			self.pageView.Close()
			self.pageView = None

	
	def destroyWithoutSave (self):
		"""
		Уничтожить панель без сохранения изменений.
		Нужно для перезагрузки вики
		"""
		if self.pageView != None:
			self.contentSizer.Detach (self.pageView)
			self.pageView.CloseWithoutSave()
			self.pageView = None
	

	def Save (self):
		"""
		Сохранить текущую страницу
		"""
		if self.pageView != None:
			self.pageView.Save()


	def __onBookmark(self, event):
		if Application.selectedPage != None:
			if not Application.selectedPage.root.bookmarks.pageMarked (Application.selectedPage):
				Application.selectedPage.root.bookmarks.add (Application.selectedPage)
			else:
				Application.selectedPage.root.bookmarks.remove (Application.selectedPage)


# end of class CurrentPagePanel



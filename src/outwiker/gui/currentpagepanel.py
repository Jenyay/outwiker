#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import wx

from outwiker.core.application import Application
from outwiker.core.factoryselector import FactorySelector
from outwiker.core.commands import pageExists, openWiki
from outwiker.core.tree import RootWikiPage
from outwiker.core.tagslist import TagsList
from outwiker.core.tagscommands import getTagsString
import outwiker.core.system


class CurrentPagePanel(wx.Panel):
    def __init__(self, *args, **kwds):
        self.__pageView = None
        self.__currentPage = None

        self.imagesDir = outwiker.core.system.getImagesDir()
        
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
        Application.onForceSave += self.__onForceSave

        self.Bind (wx.EVT_CLOSE, self.__onClose)


    @property
    def pageView (self):
        return self.__pageView


    def Print (self):
        if Application.selectedPage != None and self.__pageView != None:
            self.__pageView.Print()

    
    def __onClose (self, event):
        Application.onWikiOpen -= self.__onWikiOpen
        Application.onPageSelect -= self.__onPageSelect
        Application.onPageRename -= self.__onPageRename
        Application.onPageUpdate -= self.__onPageUpdate
        Application.onForceSave -= self.__onForceSave
        Application.onBookmarksChanged -= self.__onBookmarksChanged

        if self.__pageView != None:
            self.__pageView.Close()
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
        self.__updatePageView (page)
        self.__updatePageInfo (page)
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
        # Если новая страница имеет другой тип, то удалить старое представление и создать новое
        if type (self.__currentPage) != type (page):
            self.destroyPageView()
            self.__createPageView(page)

        # Если представление создано, то загрузим в него новую страницу
        if self.__pageView != None:
            self.__pageView.page = page

        # Запомнить страницу, чтобы потом можно было бы сравнивать ее тип с новой страницей
        self.__currentPage = page


    def __createPageView (self, page):
        """
        Создать панель просмотра для страницы
        """
        if page != None:
            factory = FactorySelector.getFactory (page.getTypeString())
            self.__pageView = factory.getPageView (self)
            self.__pageView.page = page

            assert self.__pageView != None

            self.contentSizer.Add (self.__pageView, 1, wx.EXPAND, 0)
            self.Layout()
            Application.onPageViewCreate (page)


    def __updatePageInfo (self, page):
        """
        Обновить информацию о странице
        """
        self.Freeze()
        try:
            if page != None:
                title = "%s" % (page.title)
                self.titleLabel.SetLabel (title)

                if hasattr (page, "tags"):
                    tags = u"[%s]" % getTagsString (page.tags)
                else:
                    tags = u"[]"

                self.tagsLabel.SetLabel (tags)

                self.__updateBookmarkBtn()
            else:
                self.titleLabel.SetLabel (u"")
                self.tagsLabel.SetLabel (u"[]")
            self.Layout()
        finally:
            self.Thaw()

    
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
        if self.__pageView != None:
            Application.onPageViewDestroy (self.__currentPage)

            self.contentSizer.Detach (self.__pageView)
            self.__pageView.Close()
            self.__pageView = None
            self.__currentPage = None

    
    def destroyWithoutSave (self):
        """
        Уничтожить панель без сохранения изменений.
        Нужно для перезагрузки вики
        """
        if self.__pageView != None:
            self.contentSizer.Detach (self.__pageView)
            self.__pageView.CloseWithoutSave()
            self.__pageView = None
            self.__currentPage = None
    

    def Save (self):
        """
        Сохранить текущую страницу
        """
        if self.__pageView != None:
            if not pageExists (Application.selectedPage):
                # Похоже, страница удалена вручную, перезагрузим вики
                Application.selectedPage = None
                openWiki (Application.wikiroot.path)
                return

            self.__pageView.Save()


    def __onForceSave (self):
        self.Save()


    def __onBookmark(self, event):
        if Application.selectedPage != None:
            if not Application.selectedPage.root.bookmarks.pageMarked (Application.selectedPage):
                Application.selectedPage.root.bookmarks.add (Application.selectedPage)
            else:
                Application.selectedPage.root.bookmarks.remove (Application.selectedPage)


# end of class CurrentPagePanel



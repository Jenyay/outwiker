# -*- coding: UTF-8 -*-

import os.path
import wx

from outwiker.actions.addbookmark import AddBookmarkAction
from outwiker.core.application import Application
from outwiker.core.factoryselector import FactorySelector
from outwiker.core.commands import pageExists, openWiki, MessageBox
import outwiker.core.system
from .tabsctrl import TabsCtrl


class CurrentPagePanel(wx.Panel):
    def __init__(self, *args, **kwds):
        self.__pageView = None
        self.__currentPage = None

        # Флаг обозначает, что выполняется метод Save
        self.__saveProcessing = False

        self.imagesDir = outwiker.core.system.getImagesDir()

        self.grayStarImage = os.path.join (self.imagesDir, "star_gray.png")
        self.goldStarImage = os.path.join (self.imagesDir, "star.png")

        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.tabsCtrl = TabsCtrl (self)
        self.bookmarkButton = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join (self.imagesDir, "star_gray.png"), wx.BITMAP_TYPE_ANY))

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
        if Application.selectedPage is not None and self.__pageView is not None:
            self.__pageView.Print()


    def __onClose (self, event):
        Application.onWikiOpen -= self.__onWikiOpen
        Application.onPageSelect -= self.__onPageSelect
        Application.onPageRename -= self.__onPageRename
        Application.onPageUpdate -= self.__onPageUpdate
        Application.onForceSave -= self.__onForceSave
        Application.onBookmarksChanged -= self.__onBookmarksChanged

        if self.__pageView is not None:
            self.destroyPageView()
        self.Destroy()


    def __onPageRename (self, page, oldsubpath):
        self.__onPageUpdate (page)


    def __onWikiOpen (self, root):
        self.__onPageSelect (root.selectedPage if root is not None else None)


    def __onPageSelect (self, page):
        """
        Событие при выборе страницы
        """
        if page is not None and not pageExists (page):
            MessageBox (_(u"Can't open page. Page folder not exists"), _("Error"), wx.OK | wx.ICON_ERROR)
            Application.selectedPage = None
            return

        self.Freeze()
        self.__updatePageView (page)
        self.__updatePageInfo (page)
        self.bookmarkButton.Enable (page is not None)
        self.Thaw()


    def __onPageUpdate (self, page, **kwargs):
        if Application.selectedPage is not None and Application.selectedPage == page:
            self.__updatePageInfo (page)


    def __updateBookmarkBtn (self):
        imagePath = self.grayStarImage
        tooltip = _(u"Add to Bookmarks")

        if Application.selectedPage is not None and Application.selectedPage.root.bookmarks.pageMarked (Application.selectedPage):
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
        if self.__pageView is not None:
            self.__pageView.page = page

        # Запомнить страницу, чтобы потом можно было бы сравнивать ее тип с новой страницей
        self.__currentPage = page


    def __createPageView (self, page):
        """
        Создать панель просмотра для страницы
        """
        if page is not None:
            factory = FactorySelector.getFactory (page.getTypeString())
            self.__pageView = factory.getPageView (self)
            self.__pageView.page = page

            assert self.__pageView is not None

            self.contentSizer.Add (self.__pageView, 1, wx.EXPAND, 0)
            self.Layout()
            Application.onPageViewCreate (page)


    def __updatePageInfo (self, page):
        """
        Обновить информацию о странице
        """
        self.Freeze()
        try:
            if page is not None:
                self.__updateBookmarkBtn()
            self.Layout()
        finally:
            self.Thaw()


    def __set_properties(self):
        self.bookmarkButton.SetSize(self.bookmarkButton.GetBestSize())


    def __do_layout(self):
        self.contentSizer = wx.FlexGridSizer(1, 1, 0, 0)
        self.contentSizer.AddGrowableRow(0)
        self.contentSizer.AddGrowableCol(0)
        tabsSizer = wx.FlexGridSizer(1, 0, 0, 0)
        tabsSizer.Add(self.bookmarkButton, 0,  wx.ALIGN_CENTER_VERTICAL, 0)
        tabsSizer.Add(self.tabsCtrl, 0, wx.EXPAND, 0)
        tabsSizer.AddGrowableCol(1)

        mainSizer = wx.FlexGridSizer(0, 1, 0, 0)
        mainSizer.AddGrowableRow(1)
        mainSizer.AddGrowableCol(0)
        mainSizer.Add(tabsSizer, 1, wx.EXPAND, 0)
        mainSizer.Add(self.contentSizer, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)


    def destroyPageView (self):
        """
        Уничтожить текущий контрол
        """
        if self.__pageView is not None:
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
        if self.__pageView is not None:
            Application.onPageViewDestroy (self.__currentPage)

            self.contentSizer.Detach (self.__pageView)
            self.__pageView.CloseWithoutSave()
            self.__pageView = None
            self.__currentPage = None


    def Save (self):
        """
        Сохранить текущую страницу
        """
        if self.__saveProcessing:
            return

        if self.__pageView is not None:
            if not pageExists (Application.selectedPage.root):
                # Нет папки с деревом
                self.__saveProcessing = True
                MessageBox (_(u"Can't save page. Wiki folder not exists. Wiki will be closed."), _("Error"), wx.OK | wx.ICON_ERROR)
                self.__saveProcessing = False

                Application.wikiroot = None
                return

            if not pageExists (Application.selectedPage):
                # Похоже, страница удалена вручную, перезагрузим вики
                self.__saveProcessing = True
                MessageBox (_(u"Can't save page. Page folder not exists. Wiki will be reloaded."), _("Error"), wx.OK | wx.ICON_ERROR)
                self.__saveProcessing = False

                self.__reloadWiki()
                return

            self.__pageView.Save()


    def __reloadWiki (self):
        Application.selectedPage = None
        openWiki (Application.wikiroot.path)


    def __onForceSave (self):
        self.Save()


    def __onBookmark(self, event):
        Application.actionController.getAction (AddBookmarkAction.stringId).run(None)

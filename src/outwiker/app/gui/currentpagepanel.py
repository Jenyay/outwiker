# -*- coding: utf-8 -*-

import wx

from outwiker.actions.addbookmark import AddBookmarkAction
from outwiker.core.factoryselector import FactorySelector
from outwiker.core.commands import pageExists, openWiki, showError
from outwiker.core.system import getOS, getBuiltinImagePath
from outwiker.gui.tabsctrl import TabsCtrl
from outwiker.gui.emptypageview import ClosedTreePanel
from outwiker.gui.rootpagepanel import RootPagePanel


class CurrentPagePanel(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent, style=wx.TAB_TRAVERSAL)
        self._application = application

        self.__pageView = None
        self.__currentPage = None
        self.__wikiroot = None

        self.__htmlRender = None
        self.__htmlRenderorrowed = False

        # Флаг обозначает, что выполняется метод Save
        self.__saveProcessing = False

        self.grayStarImage = getBuiltinImagePath("star_gray.png")
        self.goldStarImage = getBuiltinImagePath("star.png")

        self.tabsCtrl = TabsCtrl(self)
        self.bookmarkButton = wx.BitmapButton(
            self,
            -1,
            wx.Bitmap(getBuiltinImagePath("star_gray.png"),
                      wx.BITMAP_TYPE_ANY))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.__onBookmark, self.bookmarkButton)

        self._application.onWikiOpen += self.__onWikiOpen
        self._application.onPageSelect += self.__onPageSelect
        self._application.onBookmarksChanged += self.__onBookmarksChanged
        self._application.onForceSave += self.__onForceSave

        self.Bind(wx.EVT_CLOSE, self.__onClose)
        self.__onPageSelect(None)

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self.tabsCtrl.SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)
        self.tabsCtrl.SetForegroundColour(colour)

    def SetFocus(self):
        if self.__pageView is not None:
            self.__pageView.SetFocus()

    @property
    def pageView(self):
        return self.__pageView

    def Print(self):
        if (self._application.selectedPage is not None and
                self.__pageView is not None):
            self.__pageView.Print()

    def __onClose(self, event):
        self._application.onWikiOpen -= self.__onWikiOpen
        self._application.onPageSelect -= self.__onPageSelect
        self._application.onForceSave -= self.__onForceSave
        self._application.onBookmarksChanged -= self.__onBookmarksChanged

        if self.__pageView is not None:
            self.destroyPageView()
            # self.__pageView.Close()

        if self.__htmlRender is not None:
            self.__htmlRender.Close()
            self.__htmlRender = None
        event.Skip()

    def __onWikiOpen(self, root):
        self.__wikiroot = root
        self.__onPageSelect(root.selectedPage if root is not None else None)

    def __onPageSelect(self, page):
        """
        Событие при выборе страницы
        """
        if page is not None and not pageExists(page):
            showError(self._application.mainWindow,
                      _(u"Can't open page. Page folder not exists"))
            self.__reloadWiki()
            return

        self.__updatePageView(page)
        self.__updatePageInfo(page)
        self.bookmarkButton.Enable(page is not None)

    def __updateBookmarkBtn(self):
        imagePath = self.grayStarImage
        tooltip = _(u"Add to Bookmarks")

        page = self._application.selectedPage

        if (page is not None and
                page.root.bookmarks.pageMarked(self._application.selectedPage)):
            imagePath = self.goldStarImage
            tooltip = _(u"Remove from Bookmarks")

        self.bookmarkButton.SetBitmapLabel(wx.Bitmap(imagePath,
                                                     wx.BITMAP_TYPE_ANY))
        self.bookmarkButton.SetToolTip(tooltip)

    def __onBookmarksChanged(self, bookmarks):
        self.__updateBookmarkBtn()

    def __updatePageView(self, page):
        """
        Обновить вид страницы
        """
        # Если новая страница имеет другой тип,
        # то удалить старое представление и создать новое
        if (self.__currentPage is None or
                page is None or
                self.__currentPage.getTypeString() != page.getTypeString() or
                self.__wikiroot is None):
            self.destroyPageView()

        if self.__pageView is None:
            self.__createPageView(page)

        # Если представление создано, то загрузим в него новую страницу
        if self.__pageView is not None:
            self.__pageView.page = page
            self.__pageView.SetFocus()

        # Запомнить страницу, чтобы потом можно было бы сравнивать
        # ее тип с новой страницей
        self.__currentPage = page

    def __createPageView(self, page):
        """
        Создать панель просмотра для страницы
        """
        if page is not None:
            self.__createConcretePageView(page)
        elif page is None and self.__wikiroot is not None:
            self.__createRootPageView()
        elif self.__wikiroot is None:
            self.__createClosedTreePanel()

        if self.__pageView is not None:
            self.contentSizer.Add(self.__pageView, flag=wx.EXPAND)
            self.Layout()

            if page is not None:
                self._application.onPageViewCreate(page)

    def __createRootPageView(self):
        '''
        Create panel for selected notes root element
        '''
        self.__pageView = RootPagePanel(self, self._application)
        self.__pageView.SetBackgroundColour(self.GetBackgroundColour())
        self.__pageView.SetForegroundColour(self.GetForegroundColour())

    def __createClosedTreePanel(self):
        '''
        Create panel for closed notes tree
        '''
        self.__pageView = ClosedTreePanel(self, self._application)
        self.__pageView.SetBackgroundColour(self.GetBackgroundColour())
        self.__pageView.SetForegroundColour(self.GetForegroundColour())

    def __createConcretePageView(self, page):
        '''
        Create panel for the page self
        '''
        factory = FactorySelector.getFactory(page.getTypeString())
        pageView = factory.getPageView(self, self._application)
        pageView.SetBackgroundColour(self.GetBackgroundColour())
        pageView.SetForegroundColour(self.GetForegroundColour())
        self.__pageView = pageView
        self.__pageView.page = page

    def __updatePageInfo(self, page):
        """
        Обновить информацию о странице
        """
        self.__updateBookmarkBtn()

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

    def destroyPageView(self):
        """
        Уничтожить текущий контрол
        """
        if self.__pageView is not None:
            if self.__currentPage is not None:
                self._application.onPageViewDestroy(self.__currentPage)

            # self.contentSizer.Detach(self.__pageView)
            # wx.SafeYield(self.__pageView)
            self.__pageView.Close()
            self.__pageView = None
            self.__currentPage = None

    def destroyWithoutSave(self):
        """
        Уничтожить панель без сохранения изменений.
        Нужно для перезагрузки вики
        """
        if self.__pageView is not None:
            if self.__currentPage is not None:
                self._application.onPageViewDestroy(self.__currentPage)

            # self.contentSizer.Detach(self.__pageView)
            self.__pageView.CloseWithoutSave()
            self.__pageView = None
            self.__currentPage = None

    def Save(self):
        """
        Сохранить текущую страницу
        """
        if self.__saveProcessing:
            return

        if (self.__pageView is not None and
                self._application.selectedPage is not None):
            if not pageExists(self._application.selectedPage.root):
                # Нет папки с деревом
                self.__saveProcessing = True
                showError(self._application.mainWindow,
                          _(u"Can't save page. Wiki folder not exists. Wiki will be closed."))
                self.__saveProcessing = False

                self._application.wikiroot = None
                return

            if not pageExists(self._application.selectedPage):
                # Похоже, страница удалена вручную, перезагрузим вики
                self.__saveProcessing = True
                showError(self._application.mainWindow,
                          _(u"Can't save page. Page folder not exists. Wiki will be reloaded."))
                self.__saveProcessing = False

                try:
                    self.__reloadWiki()
                except OSError:
                    self._application.wikiroot = None

                return

            self.__pageView.Save()

    def __reloadWiki(self):
        self._application.selectedPage = None
        openWiki(self._application.wikiroot.path)

    def __onForceSave(self):
        self.Save()

    def __onBookmark(self, event):
        controller = self._application.actionController
        controller.getAction(AddBookmarkAction.stringId).run(None)

    def borrowHtmlRender(self, new_parent):
        assert not self.__htmlRenderorrowed

        if self.__htmlRender is None:
            self.__htmlRender = getOS().getHtmlRenderForPage(new_parent)
        else:
            self.__htmlRender.Awake()
            self.__htmlRender.Reparent(new_parent)

        self.__htmlRenderorrowed = True
        return self.__htmlRender

    def freeHtmlRender(self):
        assert self.__htmlRenderorrowed
        self.__htmlRenderorrowed = False
        self.__htmlRender.Sleep()
        self.__htmlRender.Reparent(self)
        self.__htmlRender.Hide()

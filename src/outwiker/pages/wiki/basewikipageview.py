# -*- coding: UTF-8 -*-

import wx
import os
from abc import ABCMeta, abstractmethod

from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.application import Application
from outwiker.core.style import Style

from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel, EVT_PAGE_TAB_CHANGED
from outwiker.core.system import readTextFile

from actions.openhtmlcode import WikiOpenHtmlCodeAction
from actions.updatehtml import WikiUpdateHtmlAction
from outwiker.pages.html.actions.switchcoderesult import SwitchCodeResultAction


class BaseWikiPageView (BaseHtmlPanel):
    __metaclass__ = ABCMeta

    HTML_RESULT_PAGE_INDEX = BaseHtmlPanel.RESULT_PAGE_INDEX + 1

    def __init__ (self, parent, *args, **kwds):
        super (BaseWikiPageView, self).__init__ (parent, *args, **kwds)

        self._application = Application

        self._hashKey = u"md5_hash"
        self.__WIKI_MENU_INDEX = 7

        # Список используемых полиморфных действий
        self.__polyActions = self._getPolyActions()

        # Список действий, которые нужно удалять с панелей и из меню.
        # А еще их надо дизаблить при переходе на вкладки просмотра результата или HTML
        self.__wikiNotationActions = self._getSpecificActions ()

        self.mainWindow.toolbars[self._getName()] = self._createToolbar (self.mainWindow)

        self.notebook.SetPageText (0, self._getPageTitle())

        self.htmlSizer = wx.FlexGridSizer(1, 1, 0, 0)
        self.htmlSizer.AddGrowableRow(0)
        self.htmlSizer.AddGrowableCol(0)

        # Номер вкладки с кодом HTML. -1, если вкладки нет
        self.htmlcodePageIndex = -1

        self._wikiMenu = wx.Menu()

        self._createCommonTools()
        self._createWikiTools()

        self._application.mainWindow.updateShortcuts()
        self.mainWindow.UpdateAuiManager()

        # Редактор с просмотром получившегося HTML (если есть)
        self.htmlCodeWindow = None

        if self._isHtmlCodeShown():
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

        self.Layout()

        self.Bind (EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)


    # Методы, которые необходимо переопределить в производном классе

    @abstractmethod
    def _getPageTitle (self):
        """
        Метод должен возвращать строку, показываемую на вкладке страницы с кодом
        """
        pass


    @abstractmethod
    def _getMenuTitle (self):
        """
        Метод должен возвращать заголовок меню
        """
        pass


    @abstractmethod
    def _createToolbar (self, mainWindow):
        """
        Метод должен возвращать экземпляр панели инструментов
        """
        pass


    @abstractmethod
    def _getPolyActions (self):
        """
        Метод должен возвращать список используемых полиморфных actions (или пустой список)
        """
        pass


    @abstractmethod
    def _getSpecificActions (self):
        """
        Метод должен возвращать список actions, которые нужно дизаблить при переходе на страницу просмотра (или пустой список)
        """
        pass


    @abstractmethod
    def _getName (self):
        """
        Метод должен возвращать имя, которое будет использоваться в названии панели инструментов
        """
        pass


    @abstractmethod
    def _getHtmlGenerator (self, page):
        """
        Метод должен возвращать экземпляр генератора, создающий код HTML для страницы
        """
        pass


    @abstractmethod
    def _getCacher (self, page, application):
        """
        Метод должен возвращать экземпляр класса, отвечающий за кэширование созданного HTML
        """
        pass


    @abstractmethod
    def _isHtmlCodeShown (self):
        """
        Возвращает True, если нужно показывать вкладку с кодом HTML, и False в противном случае
        """
        pass

    # Конец методов, которые необходимо переопределить в производном классе


    def onPreferencesDialogClose (self, prefDialog):
        super (BaseWikiPageView, self).onPreferencesDialogClose (prefDialog)
        if self.htmlCodeWindow is not None:
            self.htmlCodeWindow.setDefaultSettings()


    def onClose (self, event):
        self._removeActionTools()
        self.Unbind (EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)

        if self._getName() in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._getName())

        super (BaseWikiPageView, self).onClose (event)


    def _removeActionTools (self):
        actionController = self._application.actionController

        # Удалим элементы меню
        map (lambda action: actionController.removeMenuItem (action.stringId),
             self.__wikiNotationActions)

        # Удалим элементы меню полиморфных действий
        map (lambda strid: actionController.removeMenuItem (strid),
             self.__polyActions)

        actionController.removeMenuItem (WikiOpenHtmlCodeAction.stringId)
        actionController.removeMenuItem (WikiUpdateHtmlAction.stringId)
        actionController.removeMenuItem (SwitchCodeResultAction.stringId)

        # Удалим кнопки с панелей инструментов
        if self._getName() in self.mainWindow.toolbars:
            map (lambda action: actionController.removeToolbarButton (action.stringId),
                 self.__wikiNotationActions)

            map (lambda strid: actionController.removeToolbarButton (strid),
                 self.__polyActions)

            actionController.removeToolbarButton (WikiOpenHtmlCodeAction.stringId)
            actionController.removeToolbarButton (SwitchCodeResultAction.stringId)

        # Обнулим функции действия в полиморфных действиях
        map (lambda strid: actionController.getAction (strid).setFunc (None),
             self.__polyActions)


    @property
    def toolsMenu (self):
        return self._wikiMenu


    def __createHtmlCodePanel (self, parentSizer):
        # Окно для просмотра получившегося кода HTML
        self.htmlCodeWindow = HtmlTextEditor(self.notebook, -1)
        self.htmlCodeWindow.SetReadOnly (True)
        parentSizer.Add(self.htmlCodeWindow, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 2)

        self.addPage (self.htmlCodeWindow, _("HTML"))
        return self.pageCount - 1


    def GetSearchPanel (self):
        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            return self.codeEditor.searchPanel
        elif self.selectedPageIndex == self.htmlcodePageIndex:
            return self.htmlCodeWindow.searchPanel

        return None


    def onTabChanged (self, event):
        # import pudb; pudb.set_trace()  # XXX BREAKPOINT
        if self._currentpage is not None:
            if event.tab == self.CODE_PAGE_INDEX:
                self._onSwitchToCode()

            elif event.tab == self.RESULT_PAGE_INDEX:
                self._onSwitchToPreview()

            elif event.tab == self.htmlcodePageIndex:
                self._onSwitchCodeHtml()

            self.savePageTab(self._currentpage)

        event.Skip()


    def _enableActions (self, enabled):
        actionController = self._application.actionController

        # Активируем / дизактивируем собственные действия
        map (lambda action: actionController.enableTools (action.stringId, enabled),
             self.__wikiNotationActions)

        # Активируем / дизактивируем полиморфные действия
        map (lambda strid: actionController.enableTools (strid, enabled),
             self.__polyActions)


    def _onSwitchCodeHtml (self):
        assert self._currentpage is not None

        self._enableActions (False)
        self._updateHtmlCode ()
        self._enableAllTools ()
        self.htmlCodeWindow.SetFocus()
        self.htmlCodeWindow.Update()


    def _updateResult (self):
        super (BaseWikiPageView, self)._updateResult ()
        self._updateHtmlCode()


    def _updateHtmlCode (self):
        if self.htmlcodePageIndex == -1:
            # Нет вкладки с кодом HTML. Ничего не делаем
            return

        self.Save()
        status_item = 0
        setStatusText (_(u"Page rendered. Please wait…"), status_item)
        self._application.onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

        try:
            html = self.generateHtml (self._currentpage)
            self._showHtmlCode(html)
        except IOError as e:
            # TODO: Проверить под Windows
            MessageBox (_(u"Can't save file %s") % (unicode (e.filename)),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
        except OSError as e:
            MessageBox (_(u"Can't save HTML-file\n\n%s") % (unicode (e)),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)

        setStatusText (u"", status_item)
        self._application.onHtmlRenderingEnd (self._currentpage, self.htmlWindow)


    def _showHtmlCode (self, html):
        try:
            self.htmlCodeWindow.SetReadOnly (False)
            self.htmlCodeWindow.SetText (html)
            self.htmlCodeWindow.SetReadOnly (True)
        except IOError:
            MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)
        except OSError:
            MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)


    @abstractmethod
    def _createWikiTools (self):
        pass


    @BaseHtmlPanel.selectedPageIndex.setter
    def selectedPageIndex (self, index):
        """
        Устанавливает выбранную страницу (код, просмотр или полученный HTML)
        """
        if index == self.HTML_RESULT_PAGE_INDEX and self.htmlcodePageIndex == -1:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)
            selectedPage = self.htmlcodePageIndex
        else:
            selectedPage = index

        BaseHtmlPanel.selectedPageIndex.fset (self, selectedPage)


    def openHtmlCode (self):
        self.selectedPageIndex = self.HTML_RESULT_PAGE_INDEX


    def generateHtml (self, page):
        resultFileName = self.getHtmlPath()

        cache = self._getCacher (page, Application)
        # Проверим, можно ли прочитать уже готовый HTML
        if (cache.canReadFromCache() and os.path.exists (resultFileName)) or page.readonly:
            try:
                return readTextFile (resultFileName)
            except IOError:
                MessageBox (_(u"Can't read file {}".format (resultFileName)),
                            _(u"Error"),
                            wx.ICON_ERROR | wx.OK)
                return u""

        style = Style()
        stylepath = style.getPageStyle (page)
        generator = self._getHtmlGenerator (page)

        try:
            html = generator.makeHtml(stylepath)
            cache.saveHash()
        except IOError:
            MessageBox (_(u"Can't create HTML file"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)

        return html


    def removeGui (self):
        super (BaseWikiPageView, self).removeGui ()
        self.mainWindow.mainMenu.Remove (self.__WIKI_MENU_INDEX - 1)


    def _getAttachString (self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений

        Перегрузка метода из BaseTextPanel
        """
        text = ""
        count = len (fnames)

        for n in range (count):
            text += "Attach:" + fnames[n]
            if n != count - 1:
                text += "\n"

        return text


    def updateHtml (self):
        """
        Сбросить кэш для того, чтобы заново сделать HTML
        """
        self._getCacher (self._currentpage, Application).resetHash()

        if self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()
        elif self.selectedPageIndex == self.HTML_RESULT_PAGE_INDEX:
            self._onSwitchCodeHtml()


    def _createCommonTools (self):
        self.mainWindow.mainMenu.Insert (self.__WIKI_MENU_INDEX,
                                         self.toolsMenu,
                                         self._getMenuTitle())

        # Переключиться с кода на результат и обратно
        self._application.actionController.appendMenuItem (SwitchCodeResultAction.stringId, self.toolsMenu)
        self._application.actionController.appendToolbarButton (SwitchCodeResultAction.stringId,
                                                                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                                                                os.path.join (self.imagesDir, "render.png"),
                                                                fullUpdate=False)

        # Переключиться на код HTML
        self._application.actionController.appendMenuItem (WikiOpenHtmlCodeAction.stringId, self.toolsMenu)
        self._application.actionController.appendToolbarButton (WikiOpenHtmlCodeAction.stringId,
                                                                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                                                                os.path.join (self.imagesDir, "html.png"),
                                                                fullUpdate=False)

        # Обновить код HTML
        self._application.actionController.appendMenuItem (WikiUpdateHtmlAction.stringId, self.toolsMenu)

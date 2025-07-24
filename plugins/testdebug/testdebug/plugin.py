# -*- coding: utf-8 -*-

import os.path
import re
import logging
import time

import wx

from outwiker.api.app.application import getImagesDir
from outwiker.api.core.plugins import Plugin
from outwiker.api.core.text import positionInside
from outwiker.api.gui.hotkeys import HotKey
from outwiker.api.gui.dialogs import ButtonsDialog, MessageBox
from outwiker.api.gui.defines import TOOLBAR_PLUGINS
from outwiker.app.gui.pagedialogpanels.generalpanel import IconsGroupInfo

from .debugaction import DebugAction
from .eventswatcher import EventsWatcher
from .timer import Timer
from .tokendebug import DebugTokenFactory
from .newpagedialogpanel import NewPageDialogPanel
from .debugconfig import DebugConfig
from .pagedialogcontroller import DebugPageDialogController
from .i18n import set_


class PluginDebug(Plugin):
    def __init__(self, application):
        Plugin.__init__(self, application)
        self._url = "https://jenyay.net/Outwiker/DebugPlugin"
        self._watcher = EventsWatcher(self._application)
        self._timer = Timer()
        self._startWikiOpenTime = None
        self._prePostContentPrefix = "'''DEBUG PrePostContent'''"

    def enableFeatures(self):
        config = DebugConfig(self._application.config)

        self._enablePreProcessing = config.enablePreprocessing.value
        self._enablePostProcessing = config.enablePostprocessing.value
        self._enableOnHoverLink = config.enableOnHoverLink.value
        self._enableOnLinkClick = config.enableOnLinkClick.value
        self._enableOnEditorPopup = config.enableOnEditorPopup.value
        self._enableRenderingTimeMeasuring = config.enableRenderingTimeMeasuring.value
        self._enableNewPageDialogTab = config.enableNewPageDialogTab.value
        self._enablePageDialogEvents = config.enablePageDialogEvents.value
        self._enableOpeningTimeMeasure = config.enableOpeningTimeMeasure.value
        self._enableOnIconsGroupsListInit = config.enableOnIconsGroupsListInit.value
        self._enableOnTextEditorKeyDown = config.enableOnTextEditorKeyDown.value
        self._enableOnPrePostContent = config.enableOnPrePostContent.value
        self._enableOnTextEditorCaretMove = config.enableOnTextEditorCaretMove.value

        config.enablePreprocessing.value = self._enablePreProcessing
        config.enablePostprocessing.value = self._enablePostProcessing
        config.enableOnHoverLink.value = self._enableOnHoverLink
        config.enableOnLinkClick.value = self._enableOnLinkClick
        config.enableOnEditorPopup.value = self._enableOnEditorPopup
        config.enableRenderingTimeMeasuring.value = self._enableRenderingTimeMeasuring
        config.enableNewPageDialogTab.value = self._enableNewPageDialogTab
        config.enablePageDialogEvents.value = self._enablePageDialogEvents
        config.enableOpeningTimeMeasure.value = self._enableOpeningTimeMeasure
        config.enableOnIconsGroupsListInit.value = self._enableOnIconsGroupsListInit
        config.enableOnTextEditorKeyDown.value = self._enableOnTextEditorKeyDown
        config.enableOnPrePostContent.value = self._enableOnPrePostContent
        config.enableOnTextEditorCaretMove.value = self._enableOnTextEditorCaretMove

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext

        self.enableFeatures()
        self.__menuName = _("Debug")

        if self._application.mainWindow is not None:
            self.__createMenu()
            self.__createTestAction()

            self._application.onTreePopupMenu += self.__onTreePopupMenu
            self._application.onPostprocessing += self.__onPostProcessing
            self._application.onPreprocessing += self.__onPreProcessing
            self._application.onHoverLink += self.__onHoverLink
            self._application.onLinkClick += self.__onLinkClick
            self._application.onEditorPopupMenu += self.__onEditorPopupMenu
            self._application.onHtmlRenderingBegin += self.__onHtmlRenderingBegin
            self._application.onHtmlRenderingEnd += self.__onHtmlRenderingEnd
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onPageDialogInit += self.__onPageDialogInit
            self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
            self._application.onPageDialogPageTitleChanged += self.__onPageDialogPageTitleChanged
            self._application.onPageDialogPageStyleChanged += self.__onPageDialogPageStyleChanged
            self._application.onPageDialogPageIconChanged += self.__onPageDialogPageIconChanged
            self._application.onPageDialogPageTagsChanged += self.__onPageDialogPageTagsChanged
            self._application.onPreWikiOpen += self.__onPreWikiOpen
            self._application.onPostWikiOpen += self.__onPostWikiOpen
            self._application.onIconsGroupsListInit += self.__onIconsGroupsListInit
            self._application.onTextEditorKeyDown += self.__onTextEditorKeyDown
            self._application.onPreContentWriting += self.__onPreContentWriting
            self._application.onPostContentReading += self.__onPostContentReading
            self._application.onTextEditorCaretMove += self.__onTextEditorCaretMove

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        mainWindow = self._application.mainWindow
        mainMenu = mainWindow.menuController.getRootMenu()
        if mainWindow is not None and TOOLBAR_PLUGINS in mainWindow.toolbars:
            self._application.actionController.removeMenuItem(
                DebugAction.stringId)
            self._application.actionController.removeToolbarButton(
                DebugAction.stringId)
            self._application.actionController.removeAction(
                DebugAction.stringId)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onPluginsList)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onButtonsDialog)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onStartWatchEvents)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onStopWatchEvents)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onRaiseException)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onShowToaster)

            index = mainMenu.FindMenu(self.__menuName)
            assert index != wx.NOT_FOUND

            index = mainMenu.Remove(index)

            self._application.onTreePopupMenu -= self.__onTreePopupMenu
            self._application.onPostprocessing -= self.__onPostProcessing
            self._application.onPreprocessing -= self.__onPreProcessing
            self._application.onHoverLink -= self.__onHoverLink
            self._application.onLinkClick -= self.__onLinkClick
            self._application.onEditorPopupMenu -= self.__onEditorPopupMenu
            self._application.onHtmlRenderingBegin -= self.__onHtmlRenderingBegin
            self._application.onHtmlRenderingEnd -= self.__onHtmlRenderingEnd
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
            self._application.onPageDialogInit -= self.__onPageDialogInit
            self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
            self._application.onPageDialogPageTitleChanged -= self.__onPageDialogPageTitleChanged
            self._application.onPageDialogPageStyleChanged -= self.__onPageDialogPageStyleChanged
            self._application.onPageDialogPageIconChanged -= self.__onPageDialogPageIconChanged
            self._application.onPageDialogPageTagsChanged -= self.__onPageDialogPageTagsChanged
            self._application.onPreWikiOpen -= self.__onPreWikiOpen
            self._application.onPostWikiOpen -= self.__onPostWikiOpen
            self._application.onIconsGroupsListInit -= self.__onIconsGroupsListInit
            self._application.onTextEditorKeyDown -= self.__onTextEditorKeyDown
            self._application.onPreContentWriting -= self.__onPreContentWriting
            self._application.onPostContentReading -= self.__onPostContentReading

    def __createMenu(self):
        self.menu = wx.Menu(u"")
        pluginsListMenuItem = self.menu.Append(wx.ID_ANY,
                                               _("Plugins List"))
        buttonsDialogMenuItem = self.menu.Append(wx.ID_ANY,
                                                 _("ButtonsDialog"))
        startWatchMenuItem = self.menu.Append(wx.ID_ANY,
                                              _("Start watch events"))
        stopWatchMenuItem = self.menu.Append(wx.ID_ANY,
                                             _("Stop watch events"))
        raiseExceptionMenuItem = self.menu.Append(wx.ID_ANY,
                                                  _("Raise exception"))
        showToasterMenuItem = self.menu.Append(wx.ID_ANY,
                                               _("Show toaster"))

        self._application.mainWindow.menuController.getRootMenu().Append(self.menu,
                                                                         self.__menuName)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onPluginsList,
                                          pluginsListMenuItem)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onButtonsDialog,
                                          buttonsDialogMenuItem)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onStartWatchEvents,
                                          startWatchMenuItem)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onStopWatchEvents,
                                          stopWatchMenuItem)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onRaiseException,
                                          raiseExceptionMenuItem)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onShowToaster,
                                          showToasterMenuItem)

    def __createTestAction(self):
        mainWindow = self._application.mainWindow

        if mainWindow is not None and TOOLBAR_PLUGINS in mainWindow.toolbars:
            action = DebugAction(self._application)
            hotkey = HotKey("T", ctrl=True, shift=True, alt=True)
            toolbar = mainWindow.toolbars[TOOLBAR_PLUGINS]
            image = self.getImagePath("bug.png")

            controller = self._application.actionController

            controller.register(action, hotkey=hotkey)

            controller.appendMenuCheckItem(DebugAction.stringId, self.menu)
            controller.appendToolbarCheckButton(DebugAction.stringId,
                                                toolbar,
                                                image)

    def getImagePath(self, imageName):
        """
        Получить полный путь до картинки
        """
        imagedir = os.path.join(os.path.dirname(__file__), "images")
        fname = os.path.join(imagedir, imageName)
        return fname

    def __onTreePopupMenu(self, menu, page):
        """
        Событие срабатывает после создания всплывающего меню над деревом заметок
        """
        if page.getTypeString() == "wiki":
            menuItem = menu.Append(wx.ID_ANY, _("Message For Wiki Page"))
            menu.Bind(wx.EVT_MENU,
                      lambda event: MessageBox(
                          _("Wiki Message"), _("This is wiki page")),
                      menuItem)

        elif page.getTypeString() == "html":
            menuItem = menu.Append(wx.ID_ANY, _("Message For HTML Page"))
            menu.Bind(wx.EVT_MENU,
                      lambda event: MessageBox(
                          _("HTML Message"), _("This is HTML page")),
                      menuItem)

        elif page.getTypeString() == "text":
            menuItem = menu.Append(wx.ID_ANY, _("Message For Text Page"))
            menu.Bind(wx.EVT_MENU,
                      lambda event: MessageBox(
                          _("Text Message"), _("This is Text page")),
                      menuItem)

    def __onRaiseException(self, event):
        raise IOError

    def __onPostProcessing(self, page, params):
        if self._enablePostProcessing:
            params.result = re.compile(re.escape("абырвалг"), re.I | re.U).sub(
                "Главрыба", params.result)

    def __onPreProcessing(self, page, params):
        if self._enablePreProcessing:
            params.result = "!! Debug!!!\n" + params.result

    def __onIconsGroupsListInit(self, page, params):
        if not self._enableOnIconsGroupsListInit:
            return

        images_dir = getImagesDir()

        iconslist = [
            os.path.join(images_dir, 'add.svg'),
            os.path.join(images_dir, 'code.svg'),
            os.path.join(images_dir, 'save.png'),
        ]
        title = '__Debug group__'
        cover = None
        group_type = IconsGroupInfo.TYPE_OTHER
        sort_key = None

        newgroup = IconsGroupInfo(iconslist=iconslist,
                                  title=title,
                                  cover=cover,
                                  group_type=group_type,
                                  sort_key=sort_key)
        params.groupsList.insert(0, newgroup)

    def __onButtonsDialog(self, event):
        buttons = [_("Button 1"), _("Button 2"),
                   _("Button 3"), _("Cancel")]
        with ButtonsDialog(self._application.mainWindow,
                           _("Message"),
                           _("Caption"),
                           buttons,
                           default=0,
                           cancel=3) as dlg:
            result = dlg.ShowModal()

            if result == wx.ID_CANCEL:
                print("Cancel")
            else:
                print(result)

    def __onPluginsList(self, event):
        pluginslist = [plugin.name +
                       "\n" for plugin in self._application.plugins]
        MessageBox("".join(pluginslist), _("Plugins List"))

    def __onStartWatchEvents(self, event):
        self._watcher.startWatch()

    def __onStopWatchEvents(self, event):
        self._watcher.stopWatch()

    def __onHoverLink(self, page, params):
        if not self._enableOnHoverLink:
            return

        if params.link is None:
            return

        if params.link.startswith("http"):
            params.text = "(link) {}".format(params.text)
        elif params.link.startswith("tag://"):
            params.text = "(tag) {}".format(params.link)

    def __onLinkClick(self, page, params):
        if not self._enableOnLinkClick:
            return

        print(params.link)
        # params["process"] = True

    def __onEditorPopupMenu(self, page, params):
        if self._enableOnEditorPopup:
            params.menu.AppendSeparator()
            params.menu.Append(-1, 'Debug popup menu item')

    def __onHtmlRenderingBegin(self, page, htmlView):
        self._timer.start()

    def __onHtmlRenderingEnd(self, page, htmlView):
        assert page is not None

        if self._enableRenderingTimeMeasuring:
            interval = self._timer.getTimeInterval()
            text = 'Rendering "{page}": {time} sec'.format(
                page=page.title,
                time=interval)

            logging.info(text)

    def __onWikiParserPrepare(self, parser):
        token = DebugTokenFactory.makeDebugToken(parser)

        parser.listItemsTokens.append(token)
        parser.wikiTokens.append(token)
        parser.linkTokens.append(token)
        parser.headingTokens.append(token)
        parser.textLevelTokens.append(token)

    def __onPageDialogInit(self, page, params):
        if self._enableNewPageDialogTab:
            panel = NewPageDialogPanel(params.dialog.getPanelsParent())
            params.dialog.addPanel(panel, _('Debug'))

            controller = DebugPageDialogController(self._application)
            params.dialog.addController(controller)

    def __onPageDialogPageTypeChanged(self, page, params):
        if self._enablePageDialogEvents:
            print('Selected page type: {}'.format(params.pageType))

    def __onPageDialogPageTitleChanged(self, page, params):
        if self._enablePageDialogEvents:
            print('New page title: {}'.format(params.pageTitle))

    def __onPageDialogPageStyleChanged(self, page, params):
        if self._enablePageDialogEvents:
            print('New page style: {}'.format(params.pageStyle))

    def __onPageDialogPageIconChanged(self, page, params):
        if self._enablePageDialogEvents:
            print('New page icon: {}'.format(params.pageIcon))

    def __onPageDialogPageTagsChanged(self, page, params):
        if self._enablePageDialogEvents:
            print('New page tags: {}'.format(params.pageTags))

    def __onPreWikiOpen(self, page, params):
        if self._enableOpeningTimeMeasure:
            self._startWikiOpenTime = time.time()

    def __onPostWikiOpen(self, page, params):
        if self._enableOpeningTimeMeasure:
            interval = time.time() - self._startWikiOpenTime
            self._startWikiOpenTime = None
            text = 'Opening wiki {path}: {time} sec'.format(
                path=params.path,
                time=interval)
            logging.info(text)

    def __onTextEditorKeyDown(self, page, params):
        if self._enableOnTextEditorKeyDown:
            if params.processed:
                return

            if params.keyUnicode == ord('('):
                params.editor.turnText('(', ')')
                params.disableOutput = True
                params.processed = True

    def __onPreContentWriting(self, page, params):
        if self._enableOnPrePostContent:
            params.content = self._prePostContentPrefix + params.content

    def __onPostContentReading(self, page, params):
        if self._enableOnPrePostContent:
            if params.content.startswith(self._prePostContentPrefix):
                params.content = params.content[len(
                    self._prePostContentPrefix):]

    def __onTextEditorCaretMove(self, page, params):
        if self._enableOnTextEditorCaretMove:
            text = params.editor.GetText()
            print(params.startSelection, params.endSelection)

            if (params.startSelection == params.endSelection
                    and positionInside(text, params.startSelection, '{$', '$}')):
                print('Equation!')

    def __onShowToaster(self, event):
        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.\nPellentesque malesuada mollis tortor, eget mattis nisi lobortis et. Vestibulum accumsan vehicula volutpat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Vestibulum bibendum arcu augue, sit amet finibus augue posuere et.\nSed sem purus, fermentum et hendrerit eget, laoreet faucibus massa.'
        self._application.mainWindow.toaster.showError(text)

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "TestDebug"

    @property
    def description(self):
        return _("""Debug Plugin
                 <a href="https://jenyay.net">https://jenyay.net</a>

                 <a href="/111">Link to page</a>
                 """)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

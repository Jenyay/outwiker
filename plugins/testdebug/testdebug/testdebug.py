# -*- coding: UTF-8 -*-

import os.path
import re
import logging

import wx

from outwiker.core.commands import MessageBox
from outwiker.gui.buttonsdialog import ButtonsDialog
from outwiker.gui.hotkey import HotKey
from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS

from debugaction import DebugAction
from eventswatcher import EventsWatcher
from timer import Timer
from tokendebug import DebugTokenFactory
from newpagedialogpanel import NewPageDialogPanel
from debugconfig import DebugConfig


class PluginDebug (Plugin):
    def __init__ (self, application):
        Plugin.__init__ (self, application)
        self._url = u"http://jenyay.net/Outwiker/DebugPlugin"
        self._watcher = EventsWatcher (self._application)
        self._timer = Timer()

        self.ID_PLUGINSLIST = wx.NewId()
        self.ID_BUTTONSDIALOG = wx.NewId()
        self.ID_START_WATCH_EVENTS = wx.NewId()
        self.ID_STOP_WATCH_EVENTS = wx.NewId()


    def enableFeatures (self):
        config = DebugConfig (self._application.config)

        self._enablePreProcessing = config.enablePreprocessing.value
        self._enablePostProcessing = config.enablePostprocessing.value
        self._enableOnHoverLink = config.enableOnHoverLink.value
        self._enableOnLinkClick = config.enableOnLinkClick.value
        self._enableOnEditorPopup = config.enableOnEditorPopup.value
        self._enableOnSpellChecking = config.enableOnSpellChecking.value
        self._enableRenderingTimeMeasuring = config.enableRenderingTimeMeasuring.value
        self._enableNewPageDialogTab = config.enableNewPageDialogTab.value
        self._enablePageDialogEvents = config.enablePageDialogEvents.value

        config.enablePreprocessing.value = self._enablePreProcessing
        config.enablePostprocessing.value = self._enablePostProcessing
        config.enableOnHoverLink.value = self._enableOnHoverLink
        config.enableOnLinkClick.value = self._enableOnLinkClick
        config.enableOnEditorPopup.value = self._enableOnEditorPopup
        config.enableOnSpellChecking.value = self._enableOnSpellChecking
        config.enableRenderingTimeMeasuring.value = self._enableRenderingTimeMeasuring
        config.enableNewPageDialogTab.value = self._enableNewPageDialogTab
        config.enablePageDialogEvents.value = self._enablePageDialogEvents


    def initialize(self):
        self.enableFeatures()

        domain = u"testdebug"
        self.__ID_TREE_POPUP = wx.NewId()
        self.__ID_TRAY_POPUP = wx.NewId()

        langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"),
                           getOS().filesEncoding)
        global _

        try:
            _ = self._init_i18n (domain, langdir)
        except BaseException as e:
            print e

        self.__menuName = _(u"Debug")

        if self._application.mainWindow is not None:
            self.__createMenu()
            self.__createTestAction()

            self._application.onTreePopupMenu += self.__onTreePopupMenu
            self._application.onTrayPopupMenu += self.__onTrayPopupMenu
            self._application.onPostprocessing += self.__onPostProcessing
            self._application.onPreprocessing += self.__onPreProcessing
            self._application.onHoverLink += self.__onHoverLink
            self._application.onLinkClick += self.__onLinkClick
            self._application.onEditorPopupMenu += self.__onEditorPopupMenu
            self._application.onSpellChecking += self.__onSpellChecking
            self._application.onHtmlRenderingBegin += self.__onHtmlRenderingBegin
            self._application.onHtmlRenderingEnd += self.__onHtmlRenderingEnd
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onPageDialogInit += self.__onPageDialogInit
            self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
            self._application.onPageDialogPageTitleChanged += self.__onPageDialogPageTitleChanged


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        mainWindow = self._application.mainWindow
        if mainWindow is not None and mainWindow.PLUGINS_TOOLBAR_STR in mainWindow.toolbars:
            self._application.actionController.removeMenuItem (DebugAction.stringId)
            self._application.actionController.removeToolbarButton (DebugAction.stringId)
            self._application.actionController.removeAction (DebugAction.stringId)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onPluginsList,
                                                id=self.ID_PLUGINSLIST)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onButtonsDialog,
                                                id=self.ID_BUTTONSDIALOG)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onStartWatchEvents,
                                                id=self.ID_START_WATCH_EVENTS)

            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self.__onStopWatchEvents,
                                                id=self.ID_STOP_WATCH_EVENTS)

            index = self._application.mainWindow.mainMenu.FindMenu (self.__menuName)
            assert index != wx.NOT_FOUND

            index = self._application.mainWindow.mainMenu.Remove (index)

            self._application.onTreePopupMenu -= self.__onTreePopupMenu
            self._application.onTrayPopupMenu -= self.__onTrayPopupMenu
            self._application.onPostprocessing -= self.__onPostProcessing
            self._application.onPreprocessing -= self.__onPreProcessing
            self._application.onHoverLink -= self.__onHoverLink
            self._application.onLinkClick -= self.__onLinkClick
            self._application.onEditorPopupMenu -= self.__onEditorPopupMenu
            self._application.onSpellChecking -= self.__onSpellChecking
            self._application.onHtmlRenderingBegin -= self.__onHtmlRenderingBegin
            self._application.onHtmlRenderingEnd -= self.__onHtmlRenderingEnd
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
            self._application.onPageDialogInit -= self.__onPageDialogInit
            self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
            self._application.onPageDialogPageTitleChanged -= self.__onPageDialogPageTitleChanged


    def __createMenu (self):
        self.menu = wx.Menu (u"")
        self.menu.Append (self.ID_PLUGINSLIST, _(u"Plugins List"))
        self.menu.Append (self.ID_BUTTONSDIALOG, _(u"ButtonsDialog"))
        self.menu.Append (self.ID_START_WATCH_EVENTS, _(u"Start watch events"))
        self.menu.Append (self.ID_STOP_WATCH_EVENTS, _(u"Stop watch events"))

        self._application.mainWindow.mainMenu.Append (self.menu, self.__menuName)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onPluginsList,
                                          id=self.ID_PLUGINSLIST)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onButtonsDialog,
                                          id=self.ID_BUTTONSDIALOG)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onStartWatchEvents,
                                          id=self.ID_START_WATCH_EVENTS)

        self._application.mainWindow.Bind(wx.EVT_MENU,
                                          self.__onStopWatchEvents,
                                          id=self.ID_STOP_WATCH_EVENTS)


    def __createTestAction (self):
        mainWindow = self._application.mainWindow

        if mainWindow is not None and mainWindow.PLUGINS_TOOLBAR_STR in mainWindow.toolbars:
            action = DebugAction(self._application)
            hotkey = HotKey ("T", ctrl=True, shift=True, alt=True)
            toolbar = mainWindow.toolbars[mainWindow.PLUGINS_TOOLBAR_STR]
            image = self.getImagePath ("bug.png")

            controller = self._application.actionController

            controller.register (action, hotkey=hotkey)

            controller.appendMenuCheckItem (DebugAction.stringId, self.menu)
            controller.appendToolbarCheckButton (DebugAction.stringId,
                                                 toolbar,
                                                 image)


    def getImagePath (self, imageName):
        """
        Получить полный путь до картинки
        """
        imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
        fname = os.path.join (imagedir, imageName)
        return fname


    def __onTreePopupMenu (self, menu, page):
        """
        Событие срабатывает после создания всплывающего меню над деревом заметок
        """
        if page.getTypeString() == "wiki":
            menu.Append (self.__ID_TREE_POPUP, _(u"Message For Wiki Page"))
            menu.Bind(wx.EVT_MENU,
                      lambda event: MessageBox (_("Wiki Message"), _(u"This is wiki page")),
                      id=self.__ID_TREE_POPUP)

        elif page.getTypeString() == "html":
            menu.Append (self.__ID_TREE_POPUP, _(u"Message For HTML Page"))
            menu.Bind(wx.EVT_MENU,
                      lambda event: MessageBox (_("HTML Message"), _(u"This is HTML page")),
                      id=self.__ID_TREE_POPUP)

        elif page.getTypeString() == "text":
            menu.Append (self.__ID_TREE_POPUP, _(u"Message For Text Page"))
            menu.Bind(wx.EVT_MENU,
                      lambda event: MessageBox (_("Text Message"), _(u"This is Text page")),
                      id=self.__ID_TREE_POPUP)


    def __onTrayPopupMenu (self, menu, tray):
        menu.Insert (0, self.__ID_TRAY_POPUP, _(u"Tray Menu From Plugin"))
        menu.Bind(wx.EVT_MENU,
                  lambda event: MessageBox (_("Tray Icon"), _(u"This is tray icon")),
                  id=self.__ID_TRAY_POPUP)


    def __onPostProcessing (self, page, params):
        if self._enablePostProcessing:
            params.result = re.compile(re.escape(u"абырвалг"), re.I | re.U).sub (u"Главрыба", params.result)


    def __onPreProcessing (self, page, params):
        if self._enablePreProcessing:
            params.result = "!! Debug!!!\n" + params.result


    def __onButtonsDialog (self, event):
        buttons = [_(u"Button 1"), _(u"Button 2"), _(u"Button 3"), _(u"Cancel")]
        with ButtonsDialog (self._application.mainWindow,
                            _(u"Message"),
                            _(u"Caption"),
                            buttons,
                            default=0,
                            cancel=3) as dlg:
            result = dlg.ShowModal()

            if result == wx.ID_CANCEL:
                print u"Cancel"
            else:
                print result


    def __onPluginsList (self, event):
        pluginslist = [plugin.name + "\n" for plugin in self._application.plugins]
        MessageBox (u"".join (pluginslist), _(u"Plugins List"))


    def __onStartWatchEvents (self, event):
        self._watcher.startWatch()


    def __onStopWatchEvents (self, event):
        self._watcher.stopWatch()


    def __onHoverLink (self, page, params):
        if not self._enableOnHoverLink:
            return

        if params.link is None:
            return

        if params.link.startswith (u"http"):
            params.text = u"(link) {}".format (params.text)
        elif params.link.startswith (u"tag://"):
            params.text = u"(tag) {}".format (params.link)


    def __onLinkClick (self, page, params):
        if not self._enableOnLinkClick:
            return

        print params.link
        # params["process"] = True


    def __onEditorPopupMenu (self, page, params):
        if self._enableOnEditorPopup:
            params.menu.AppendSeparator()
            params.menu.Append (-1, u'Debug popup menu item')


    def __onSpellChecking (self, page, params):
        if self._enableOnSpellChecking:
            if params.word.lower() == u'хрень':
                params.isValid = False
            elif params.word.lower() == u'блаблабла':
                params.isValid = True


    def __onHtmlRenderingBegin (self, page, htmlView):
        self._timer.start()


    def __onHtmlRenderingEnd (self, page, htmlView):
        assert page is not None

        if self._enableRenderingTimeMeasuring:
            interval = self._timer.getTimeInterval()
            text = u'Rendering "{page}": {time} sec'.format (
                page = page.title,
                time = interval)

            logging.info (text)


    def __onWikiParserPrepare (self, parser):
        token = DebugTokenFactory.makeDebugToken(parser)

        parser.listItemsTokens.append (token)
        parser.wikiTokens.append (token)
        parser.linkTokens.append (token)
        parser.headingTokens.append (token)
        parser.textLevelTokens.append (token)


    def __onPageDialogInit (self, page, params):
        if self._enableNewPageDialogTab:
            panel = NewPageDialogPanel (params.dialog.getPanelsParent(),
                                        self._application)
            params.dialog.addPanel (panel)


    def __onPageDialogPageTypeChanged (self, page, params):
        if self._enablePageDialogEvents:
            print params.pageType


    def __onPageDialogPageTitleChanged (self, page, params):
        if self._enablePageDialogEvents:
            print params.pageTitle


    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name (self):
        return u"Debug Plugin"


    @property
    def description (self):
        return _(u"""Debug Plugin
                 <a href="http://jenyay.net">http://jenyay.net</a>

                 <a href="/111">Link to page</a>
                 """)


    @property
    def version (self):
        return u"0.5"


    @property
    def url (self):
        return self._url


    @url.setter
    def url (self, value):
        self._url = value

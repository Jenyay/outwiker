# -*- coding: utf-8 -*-

import logging

from outwiker.core.config import Config
from outwiker.core.event import Event, CustomEvents
from outwiker.core.events import PostWikiCloseParams, PreWikiCloseParams
from outwiker.core.recent import RecentWiki
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.pageuiddepot import PageUidDepot
from outwiker.gui.theme import Theme

logger = logging.getLogger('outwiker.core.application')


class Application:
    def __init__(self):
        # Opened wiki
        self.__wikiroot = None

        # Application's main window
        self.__mainWindow = None

        # Application's global config
        self.config = None
        self.recentWiki = None
        self.actionController = None
        self.plugins = PluginsLoader(self)
        self.pageUidDepot = PageUidDepot()
        self.__theme = Theme()

        # Set to True for unit tests
        self.testMode = False

        # Values for shared purpose
        self.sharedData = {}

        self.customEvents = CustomEvents()

        # Events

        # Opening wiki event
        # Parameters:
        #     root - opened wiki root (it may be None)
        self.onWikiOpen = Event()

        # Closing wiki event
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the outwiker.core.events.PreWikiCloseParams
        #              class
        self.onPreWikiClose = Event()

        # Updating page wiki event
        # Parameters:
        #     page - updated page
        #     **kwargs
        # kwargs contain 'change' key, which contain changing flags
        self.onPageUpdate = Event()

        # Creating new wiki page
        # Parameters:
        #     sender - new page
        self.onPageCreate = Event()

        # Tree updating event
        # Parameters:
        #     sender - Page, because of which the tree is updated.
        self.onTreeUpdate = Event()

        # Other page selection event
        # Parameters:
        #     sender - selected page
        self.onPageSelect = Event()

        # User want insert link to selected attachments to page
        # Parameters:
        #     fnames - selected file names (names only, without full paths)
        self.onAttachmentPaste = Event()

        # Changings in the bookmarks list event
        # Parameters:
        #     params - instance of BookmarksChangedParams
        self.onBookmarksChanged = Event()

        # Removing the page event
        # Parameters:
        #     page - page is removed
        self.onPageRemove = Event()

        # Renaming page event
        # Parameters:
        #     page - page is renamed,
        #     oldSubpath - previous relative path to page
        self.onPageRename = Event()

        # Beginning complex tree updating (updating of several steps) event
        # Parameters:
        #     root - wiki tree root
        self.onStartTreeUpdate = Event()

        # Finishing complex tree updating (updating of several steps) event
        # Parameters:
        #     root - wiki tree root
        self.onEndTreeUpdate = Event()

        # Beginning HTML rendering event
        # Parameters:
        #   page - rendered page
        #   htmlView - window for HTML view
        self.onHtmlRenderingBegin = Event()

        # Finishing HTML rendering event
        # Parameters:
        #   page - rendered page
        #   htmlView - window for HTML view
        self.onHtmlRenderingEnd = Event()

        # Changing page order event
        # Parameters:
        #     page - page with changed order
        self.onPageOrderChange = Event()

        # Evont for forced saving page state
        # (e.g. by the loss the focus or by timer)
        # Parameters:
        #     --
        self.onForceSave = Event()

        # The event occurs after wiki parser (Parser class) creation,
        # but before it using
        # Parameter:
        #     parser - Parser class instance
        self.onWikiParserPrepare = Event()

        # Event occurs during preferences dialog creation
        # Parameters:
        #     dialog - outwiker.gui.preferences.prefdialog.PrefDialog
        #              class instance
        self.onPreferencesDialogCreate = Event()

        # Event occurs after preferences dialog closing.
        # Parameters:
        #     dialog - outwiker.gui.preferences.prefdialog.PrefDialog
        #              class instance
        self.onPreferencesDialogClose = Event()

        # Event occurs after (!) the page view creation
        # (inside CurrentPagePanel instance)
        # Parameters:
        #     page - new selected page
        self.onPageViewCreate = Event()

        # Event occurs before(!) the page view removing
        # (inside CurrentPagePanel instance)
        # Parameters:
        #     page - Current selected page
        self.onPageViewDestroy = Event()

        # Event occurs after the popup menu creation by right mouse click
        # on the notes tree
        # Parameters:
        #     menu - created popup menu,
        #     page - the page on which was right clicked in the notes tree
        self.onTreePopupMenu = Event()

        # Event occurs before HTML generation (for wiki and HTML pages)
        # Order of the calling preprocessing events is not regulated
        # Parameters:
        #    page - page for which HTML is generated
        #    params - instance of the outwiker.core.events.PreprocessingParams
        #             class
        self.onPreprocessing = Event()

        # Event occurs after HTML generation (for wiki and HTML pages)
        # Order of the calling preprocessing events is not regulated
        # Parameters:
        #    page - page for which HTML is generated
        #    params - instance of the outwiker.core.events.PostprocessingParams
        #             class
        self.onPostprocessing = Event()

        # Event occurs after wiki parsing but before HTML improving
        # Parameters:
        #     page - page for which HTML is generated
        #     params - instance of the
        #              outwiker.core.events.PreHtmlImprovingParams class
        self.onPreHtmlImproving = Event()

        # Event occurs during HtmlImproverFactory instance creation
        # Parameters:
        #     factory - HtmlImproverFactory instance in which can add
        #     the new HtmlImprover instances by add() method
        self.onPrepareHtmlImprovers = Event()

        # Event occurs when cursor hovers under link on preview tab
        # Parameters:
        #     page - current page
        #     params - instance of the outwiker.core.events.HoverLinkParams
        #              class
        self.onHoverLink = Event()

        # Event occurs when user click to link on a page
        # Parameters:
        #     page - current page
        #     params - instance of the outwiker.core.events.LinkClickParams
        #              class
        self.onLinkClick = Event()

        # Event occurs when user click with right button in text editor
        # Parameters:
        #     page - current page
        #     params - instance of the the
        #              outwiker.core.events.EditorPopupMenuParams class
        self.onEditorPopupMenu = Event()

        # Event occurs after page dialog creation
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogInitParams class
        self.onPageDialogInit = Event()

        # Event occurs before page dialog will be destroyed
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogDestroyParams class
        self.onPageDialogDestroy = Event()

        # Event occurs after page type changing
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogPageTypeChangedParams class
        self.onPageDialogPageTypeChanged = Event()

        # Event occurs after page type changing
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogPageTitleChangedParams class
        self.onPageDialogPageTitleChanged = Event()

        # Event occurs after new page order changing
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogNewPageOrderChangedParams class
        self.onPageDialogNewPageOrderChanged = Event()

        # Event occurs after page style changing
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogPageStyleChangedParams class
        self.onPageDialogPageStyleChanged = Event()

        # Event occurs after page icon changing
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogPageIconChangedParams class
        self.onPageDialogPageIconChanged = Event()

        # Event occurs after page tag list changing
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogPageTagsChangedParams class
        self.onPageDialogPageTagsChanged = Event()

        # Event occurs during page dialog initialization,
        # during general panel creation. Evens sender expect what event
        # handlers will fill the page factories list with addPageFactory method
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageDialogPageFactoriesNeededParams
        #              class
        self.onPageDialogPageFactoriesNeeded = Event()

        # Event occurs by TextEditor when it needs styles
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the EditorStyleNeededParams class
        self.onEditorStyleNeeded = Event()

        # Event forces update and render current page
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageUpdateNeededParams class
        self.onPageUpdateNeeded = Event()

        # Event occurs before wiki opening
        # Parameters:
        #    page - current (selected) page
        #    params - instance of the PreWikiOpenParams class
        self.onPreWikiOpen = Event()

        # Event occurs after wiki opening
        # Parameters:
        #    page - current (selected) page
        #    params - instance of the PostWikiOpenParams class
        self.onPostWikiOpen = Event()

        # Event occurs after wiki closing
        # Parameters:
        #    params - instance of the PostWikiCloseParams class
        self.onPostWikiClose = Event()

        # Event occurs in the IconsPanel after generation list of
        # the icons groups.
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the IconsGroupsListInitParams class
        self.onIconsGroupsListInit = Event()

        # Event occurs after switch mode of a page: text / preview / HTML / ...
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PageModeChangeParams class
        self.onPageModeChange = Event()

        # Event occurs after change attachments list.
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the AttachListChangedParams class
        self.onAttachListChanged = Event()

        # Event occurs after opening subdirectory in attachments
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the AttachSubdirChangedParams class
        self.onAttachSubdirChanged = Event()

        # Event occurs after key pressing in the notes text editor
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the TextEditorKeyDownParams class
        self.onTextEditorKeyDown = Event()

        # Event occurs after caret moving in a text editor
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the TextEditorCaretMoveParams class
        self.onTextEditorCaretMove = Event()

        # Event occurs after page content reading. The content can be changed
        # by event handlers
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PostContentReadingParams class
        self.onPostContentReading = Event()

        # Event occurs before page content writing. The content can be changed
        # by event handlers
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the PreContentWritingParams class
        self.onPreContentWriting = Event()

        # Need for attachment renaming.
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the BeginAttachRenamingParams class
        self.onBeginAttachRenaming = Event()

        # Event occurs after selection / clear selection attachments
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the AttachSelectionChangedParams class
        self.onAttachSelectionChanged = Event()

        # Event occurs after list of visible the notes tree items
        # Parameters:
        #    page - current (selection) page
        #    params - instance of the NotesTreeItemsPreparingParams class
        self.onNotesTreeItemsPreparing = Event()

        # The event denotes that the notes tree items should be updated:
        # Parameters:
        #    page - current (selection) page
        #    params - instance of the ForceNotesTreeItemsUpdate class
        self.onForceNotesTreeItemsUpdate = Event()

    def init(self, fullConfigPath):
        """
        Initialize config and locale
        """
        self.fullConfigPath = fullConfigPath
        self.config = Config(fullConfigPath)
        self.recentWiki = RecentWiki(self.config)
        self.__theme.loadFromConfig(self.config)

    def clear(self):
        if self.wikiroot is not None:
            self.__unbindWikiEvents(self.wikiroot)

        self._unbindAllEvents()
        self.__theme.clear()
        self.wikiroot = None
        self.config = None
        self.mainWindow = None

    def _unbindAllEvents(self):
        for member_name in sorted(dir(self)):
            member = getattr(self, member_name)
            if isinstance(member, Event):
                member.clear()

        for key in list(self.customEvents.getKeys()):
            self.customEvents.clear(key)

    @property
    def theme(self) -> Theme:
        return self.__theme

    @property
    def wikiroot(self):
        """
        Return the root of the wiki opened in the current time or None if
        no wiki opened
        """
        return self.__wikiroot

    @wikiroot.setter
    def wikiroot(self, value):
        """
        Set wiki as current
        """
        if self.__wikiroot is not None:
            wikiPath = self.__wikiroot.path

            preWikiCloseParams = PreWikiCloseParams(self.__wikiroot)
            self.onPreWikiClose(self.selectedPage, preWikiCloseParams)
            if preWikiCloseParams.abortClose:
                logger.debug('Wiki closing aborted: %s', wikiPath)
                return

            self.__unbindWikiEvents(self.__wikiroot)
            try:
                self.__wikiroot.save()
            except OSError:
                logger.error("Can't save notes tree settings: %s", self.__wikiroot.path)
                self.__wikiroot = None

            postWikiCloseParams = PostWikiCloseParams(wikiPath)
            self.onPostWikiClose(postWikiCloseParams)

        self.__wikiroot = value

        if self.__wikiroot is not None:
            self.__bindWikiEvents(self.__wikiroot)

        self.pageUidDepot = PageUidDepot(self.__wikiroot)
        self.onWikiOpen(self.__wikiroot)

    @property
    def mainWindow(self):
        """
        Return main window instance or None if main window is not created
        """
        return self.__mainWindow

    @mainWindow.setter
    def mainWindow(self, value):
        """
        Set main window for the program
        """
        self.__mainWindow = value

    def __bindWikiEvents(self, wiki):
        """
        Subscribe to wiki event to forward it to next receiver.
        """
        wiki.onPageSelect += self.onPageSelect
        wiki.onPageUpdate += self.onPageUpdate
        wiki.onTreeUpdate += self.onTreeUpdate
        wiki.onStartTreeUpdate += self.onStartTreeUpdate
        wiki.onEndTreeUpdate += self.onEndTreeUpdate
        wiki.onPageOrderChange += self.onPageOrderChange
        wiki.onPageRename += self.onPageRename
        wiki.onPageCreate += self.onPageCreate
        wiki.onPageRemove += self.onPageRemove
        wiki.onAttachListChanged += self.onAttachListChanged
        wiki.onAttachSubdirChanged += self.onAttachSubdirChanged
        wiki.bookmarks.onBookmarksChanged += self.onBookmarksChanged
        wiki.onPostContentReading += self.onPostContentReading
        wiki.onPreContentWriting += self.onPreContentWriting

    def __unbindWikiEvents(self, wiki):
        """
        Unsubscribe from wiki events.
        """
        wiki.onPageSelect -= self.onPageSelect
        wiki.onPageUpdate -= self.onPageUpdate
        wiki.onTreeUpdate -= self.onTreeUpdate
        wiki.onStartTreeUpdate -= self.onStartTreeUpdate
        wiki.onEndTreeUpdate -= self.onEndTreeUpdate
        wiki.onPageOrderChange -= self.onPageOrderChange
        wiki.onPageRename -= self.onPageRename
        wiki.onPageCreate -= self.onPageCreate
        wiki.onPageRemove -= self.onPageRemove
        wiki.onAttachListChanged -= self.onAttachListChanged
        wiki.onAttachSubdirChanged -= self.onAttachSubdirChanged
        wiki.bookmarks.onBookmarksChanged -= self.onBookmarksChanged
        wiki.onPostContentReading -= self.onPostContentReading
        wiki.onPreContentWriting -= self.onPreContentWriting

    @property
    def selectedPage(self):
        """
        Return the instance of the selected page or None if no selected page.
        """
        if self.__wikiroot is None:
            return None

        return self.__wikiroot.selectedPage

    @selectedPage.setter
    def selectedPage(self, page):
        """
        Set page as selected
        """
        if (self.__wikiroot is not None and
                self.__wikiroot.selectedPage != page):
            self.__wikiroot.selectedPage = page

    def getEvent(self, name):
        """Return build-in event or custom event"""
        if hasattr(self, name) and isinstance(getattr(self, name), Event):
            return getattr(self, name)
        return self.customEvents.get(name)

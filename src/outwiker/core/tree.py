# -*- coding: utf-8 -*-

import logging
import os
import os.path
import shutil
import datetime
from abc import ABCMeta
from typing import Any, Callable, final, List, Optional, Union, Dict
import uuid

from .config import PageConfig
from .event import Event
from .exceptions import (
    ClearConfigError,
    DuplicateTitle,
    ReadonlyException,
    TreeException,
)
from .defines import (
    PAGE_CONTENT_FILE,
    PAGE_OPT_FILE,
    REGISTRY_FILE,
)
from .iconcontroller import IconController
from .system import getIconsDirList
from .registrynotestree import NotesTreeRegistry, PickleSaver
from . import events
from outwiker.utilites.textfile import readTextFile, writeTextFile


logger = logging.getLogger("core")


class BasePage(metaclass=ABCMeta):
    """
    Base class for note page or for root page
    """

    def __init__(self, path: str, readonly: bool = False):
        # Path to page
        self._path = path
        self._parent: Optional[BasePage] = None
        self._children: List[WikiPage] = []
        self.readonly = readonly
        self._typeString = None

        self._expanded: Optional[bool] = None
        # Option name for registry about expand state
        self._expanded_option_name = "Expand"

        configpath = os.path.join(path, PAGE_OPT_FILE)
        if (
            not self.readonly
            and os.path.exists(configpath)
            and not os.access(configpath, os.W_OK)
        ):
            self.readonly = True

        self._params = BasePage.readParams(self.path, self.readonly)
        self._datetime = self._getDateTime()

    def getTypeString(self) -> Optional[str]:
        if self._typeString is None:
            self._typeString = self._params.typeOption.value

        return self._typeString

    def setTypeString(self, typeString):
        self._typeString = typeString
        self.save()

    @staticmethod
    def readParams(path: str, readonly: bool = False) -> PageConfig:
        return PageConfig(os.path.join(path, PAGE_OPT_FILE), readonly)

    @property
    def params(self) -> PageConfig:
        return self._params

    @property
    def path(self) -> str:
        return self._path

    @property
    def parent(self) -> Optional["BasePage"]:
        return self._parent

    @property
    def children(self) -> List["WikiPage"]:
        return self._children[:]

    @children.setter
    def children(self, children: List["WikiPage"]):
        self._children = children

    @property
    def root(self) -> "WikiDocument":
        """
        Return root of note tree
        """
        result = self
        while result.parent is not None:
            result = result.parent

        return result

    def isExpanded(self) -> bool:
        if self._expanded is None:
            page_registry = self.root.registry.get_page_registry(self)
            self._expanded = page_registry.getbool(
                self._expanded_option_name, default=False
            )
        return self._expanded

    def expand(self, expanded: bool):
        self._expanded = expanded
        if not self.readonly:
            page_registry = self.root.registry.get_page_registry(self)
            page_registry.set(self._expanded_option_name, expanded)

    def save(self):
        if self.readonly:
            return

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self._params.save()

    def __len__(self) -> int:
        return len(self._children)

    def __getitem__(self, path: str) -> Optional[Union["BasePage", "WikiPage"]]:
        """
        Get page by relative path in tree
        """
        if len(path) == 0:
            return None

        if path == "/":
            return self.root

        # If path starts with "/", count starts from root
        if path[0] == "/":
            return self.root[path[1:]]

        # Split path into its constituent parts
        titles = path.split("/")
        page = self

        for title in titles:
            found = False
            if title == "..":
                page = page.parent
                found = page is not None
            else:
                title_lower = title.lower()
                for child in page.children:
                    if (
                        child.title.lower() == title_lower
                        or child.display_title.lower() == title_lower
                    ):
                        page = child
                        found = True

            if not found:
                page = None
                break

        return page

    def sortChildren(
        self, key_func: Callable[["WikiPage"], Any], reverse: bool = False
    ):
        """
        Sort children pages
        """
        self._children.sort(key=key_func, reverse=reverse)

        self.root.onStartTreeUpdate(self.root)
        self.saveChildrenParams()
        self.root.onEndTreeUpdate(self.root)

    @staticmethod
    def testDublicate(parent, title):
        """
        Check that parent does not have a page with such title
        """
        for page in parent.children:
            if page.title.lower() == title.lower():
                return False
        return True

    def changeChildOrder(self, page, neworder):
        """
        Change the order of child elements
        Move the child page 'page' to the level 'neworder'
        """
        oldorder = self._children.index(page)
        if oldorder == neworder:
            return

        if page.readonly:
            raise ReadonlyException(page)

        realorder = neworder

        if realorder < 0:
            realorder = 0

        if realorder >= len(self.children):
            realorder = len(self.children) - 1

        if oldorder != realorder:
            self.removeFromChildren(page)
            self._children.insert(realorder, page)
            self.saveChildrenParams()
            self.root.onPageOrderChange(page)

    def saveChildrenParams(self):
        for child in self._children:
            child.save()

    def addToChildren(self, page, order):
        """
        Add the page to children
        """
        self._children.insert(order, page)

    def removeFromChildren(self, page):
        """
        Remove the page from children
        """
        self._children.remove(page)

    def isChild(self, page):
        """
        Check if 'page' is a child (nested) page of 'self'
        """
        currentpage = page
        while currentpage is not None:
            if currentpage == self:
                return True
            currentpage = currentpage.parent

        return False

    @property
    def datetime(self):
        """
        Get the date and time of page modification as a datetime.datetime instance
        """
        return self._datetime

    def _getDateTime(self):
        date = self.params.datetimeOption.value
        if date is None:
            # If date is not set, return the date of the last modification of the content file,
            # and write this date to the settings file
            contentpath = os.path.join(self.path, PAGE_CONTENT_FILE)
            if os.path.exists(contentpath):
                time = os.path.getmtime(contentpath)
                date = datetime.datetime.fromtimestamp(time)
                self.datetime = date

        return date

    @datetime.setter
    def datetime(self, date):
        self.params.datetimeOption.value = date
        self._datetime = date

    @property
    def creationdatetime(self):
        date = self.params.creationDatetimeOption.value
        if date is None:
            date = self.datetime
            self.creationdatetime = date

        return date

    @creationdatetime.setter
    def creationdatetime(self, date):
        self.params.creationDatetimeOption.value = date

    def updateDateTime(self):
        """
        Set the page modification date to the current date/time
        """
        self.datetime = datetime.datetime.now()

    def update(self):
        """
        Update page content if needed.
        The method can raise EnvironmentError.
        """

    def getUid(self, generate: bool = True) -> Optional[str]:
        return ""

    def setUid(self, new_uid: str) -> None:
        pass


@final
class WikiDocument(BasePage):
    def __init__(self, path, readonly=False):
        super().__init__(path, readonly)
        self._selectedPage = None
        self._createEvents()
        self._registry = NotesTreeRegistry(self._getRegistrySaver(self._path))
        self._pageUidDepot = PageUidDepot()
        self._typeString = "document"

    def _getRegistrySaver(self, path):
        registry_path = os.path.join(path, REGISTRY_FILE)
        return PickleSaver(registry_path)

    def _createEvents(self):
        # New page selection
        # Parameters: new selected page
        self.onPageSelect = Event()

        # Tree update
        # Parameters: sender - who triggers the tree update
        self.onTreeUpdate = Event()

        # Start of complex tree update
        # Parameters: root - tree root
        self.onStartTreeUpdate = Event()

        # End of complex tree update
        # Parameters: root - tree root
        self.onEndTreeUpdate = Event()

        # Page update
        # Parameters:
        #     sender
        #     **kwargs
        # kwargs contains the 'change' value, storing flags for what changed
        self.onPageUpdate = Event()

        # Changing page order
        # Parameters: page - the page whose position was changed
        self.onPageOrderChange = Event()

        # Page rename.
        # Parameters:
        #   page - the renamed page,
        #   oldSubpath - old relative path to the page
        self.onPageRename = Event()

        # Page creation
        # Parameters: sender
        self.onPageCreate = Event()

        # Page deletion
        # Parameter - the deleted page
        self.onPageRemove = Event()

        # Event occurs after change attached file list.
        # Parameters:
        #     page - current (selected) page
        #     params - instance if the AttachListChangedParams class
        self.onAttachListChanged = Event()

        # Event occurs after opening subdirectory in attachments
        # Parameters:
        #     page - current (selected) page
        #     params - instance of the AttachSubdirChangedParams class
        self.onAttachSubdirChanged = Event()

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

    @property
    def pageUidDepot(self) -> "PageUidDepot":
        return self._pageUidDepot

    def updatePageUidDepot(self):
        self._pageUidDepot.load(self)

    @staticmethod
    def clearConfigFile(path):
        """
        Clear the __page.opt file.
        Used in case the __page.opt file is corrupted.
        path - path to wiki (or to directory with __page.opt file, or including this file)
        """
        if path.endswith(PAGE_OPT_FILE):
            realpath = path
        else:
            realpath = os.path.join(path, PAGE_OPT_FILE)

        try:
            fp = open(realpath, "w", encoding="utf8")
            fp.close()
        except IOError:
            raise ClearConfigError

    def save(self):
        super().save()
        self._registry.save()

    @staticmethod
    def create(path):
        """
        Create root for wiki
        """
        root = WikiDocument(path)
        root.save()
        root.onTreeUpdate(root)

        return root

    @property
    def selectedPage(self):
        return self._selectedPage

    @selectedPage.setter
    def selectedPage(self, page):
        if page is None or page.getTypeString() == self.getTypeString():
            # Cannot select WikiDocument class instance
            self._selectedPage = None
        else:
            self._selectedPage = page

        self.root.onPageSelect(self._selectedPage)
        self.save()

    @property
    def subpath(self):
        return "/"

    @property
    def display_subpath(self):
        return "/"

    @property
    def title(self):
        return os.path.basename(self.path)

    @property
    def display_title(self):
        return self.title

    @property
    def registry(self):
        return self._registry

    def getPageByUid(self, uid: str) -> Optional[BasePage]:
        return self._pageUidDepot[uid]


class WikiPage(BasePage, metaclass=ABCMeta):
    """
    Page in tree.
    """

    iconController = IconController(getIconsDirList()[0])

    def __init__(self, path, title, parent, readonly=False):
        """
        Constructor.

        path -- path to page
        """
        if not BasePage.testDublicate(parent, title):
            logger.error(
                "Duplicate page title in the parent page. Title: %s. Parent: %s",
                title,
                parent.subpath,
            )
            raise DuplicateTitle

        super().__init__(path, readonly)
        self._DEFAULT_ATTACH_SUBDIR = ""
        self._attach_subdir = self._DEFAULT_ATTACH_SUBDIR
        self._title = title
        self._parent = parent
        self._tags = [tag for tag in self.params.tagsOption.value if tag]
        self._alias = self.params.aliasOption.value

        if len(self._alias) == 0:
            self._alias = None
        self._uid = self.params.pageUidOption.value

    def __bool__(self):
        return True

    @property
    def currentAttachSubdir(self) -> str:
        return self._attach_subdir

    @currentAttachSubdir.setter
    def currentAttachSubdir(self, value: str):
        if not value or value == ".":
            value = self._DEFAULT_ATTACH_SUBDIR

        self._attach_subdir = value
        self.root.onAttachSubdirChanged(self, events.AttachSubdirChangedParams())

    def isCurrentAttachSubdirRoot(self):
        return self._attach_subdir == self._DEFAULT_ATTACH_SUBDIR

    @property
    def order(self):
        """
        Return the page index in the list of child pages
        """
        return self.parent.children.index(self)

    @order.setter
    def order(self, neworder):
        """
        Change the page position (order)
        """
        self.parent.changeChildOrder(self, neworder)

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value):
        if self._alias == value:
            return

        if self.readonly:
            raise ReadonlyException(self)

        if self._alias == value:
            return

        if not value:
            self._alias = None
            self.params.aliasOption.remove_option()
        else:
            self._alias = value
            self.params.aliasOption.value = value

        self.root.onPageUpdate(self, change=events.PAGE_UPDATE_TITLE)

    @property
    def display_title(self):
        return self.alias if self.alias else self.title

    @display_title.setter
    def display_title(self, value):
        if not value:
            self.alias = None
        elif self.alias is not None:
            self.alias = value
        else:
            self.title = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, newtitle):
        if self._title == newtitle:
            return

        if self.readonly:
            raise ReadonlyException(self)

        oldtitle = self.title
        oldpath = self.path
        oldsubpath = self.subpath

        if oldtitle == newtitle:
            return

        # Check for duplicate pages and that only the letter case can be changed in the page title
        if not self.canRename(newtitle):
            raise DuplicateTitle

        newpath = os.path.join(os.path.dirname(oldpath), newtitle)
        os.renames(oldpath, newpath)
        self._title = newtitle

        WikiPage._renamePaths(self, newpath)
        self.root.registry.rename_page_sections(oldsubpath, self.subpath)
        self.updateDateTime()

        self.root.onPageRename(self, oldsubpath)
        self.root.onPageUpdate(self, change=events.PAGE_UPDATE_TITLE)

    def canRename(self, newtitle):
        return self.title.lower() == newtitle.lower() or self.parent[newtitle] is None

    @staticmethod
    def _renamePaths(page, newPath):
        """
        Correct paths after renaming a page
        """
        oldPath = page.path
        page._path = newPath
        page._params = BasePage.readParams(page.path)

        for child in page.children:
            newChildPath = child.path.replace(oldPath, newPath, 1)
            WikiPage._renamePaths(child, newChildPath)

    def moveTo(self, newparent):
        """
        Move the entry to another parent
        """
        if self._parent == newparent:
            return

        if self.readonly or newparent.readonly:
            raise ReadonlyException(self)

        if self.isChild(newparent):
            # Cannot be a parent of one's own parent (ancestor)
            raise TreeException

        # Check that the new parent does not have an entry with the same title
        if newparent[self.title] is not None:
            raise DuplicateTitle

        oldpath = self.path
        oldparent = self.parent
        oldsubpath = self.subpath

        # New path for the page
        newpath = os.path.join(newparent.path, self.title)

        # Temporary folder name.
        # First, we'll try renaming the folder with the page, and then move it to the right place with the right name
        tempname = self._getTempName(oldpath)

        try:
            os.renames(oldpath, tempname)
            shutil.move(tempname, newpath)
        except shutil.Error:
            raise TreeException
        except OSError:
            raise TreeException

        self._parent = newparent
        oldparent.removeFromChildren(self)
        newparent.addToChildren(self, len(newparent.children))

        newsubpath = self.subpath
        WikiPage._renamePaths(self, newpath)
        self.root.registry.rename_page_sections(oldsubpath, newsubpath)

        self.root.onTreeUpdate(self)

    def _getTempName(self, pagepath):
        """
        Find a unique name for the moved page.
        When moving, first try renaming the folder with the page, then move it.

        pagepath - current path to page

        The method returns the full path
        """
        path, title = os.path.split(pagepath)
        template = "__{title}_{number}"
        number = 0
        newname = template.format(title=title, number=number)

        while os.path.exists(os.path.join(path, newname)):
            number += 1
            newname = template.format(title=title, number=number)

        return os.path.join(path, newname)

    @property
    def icon(self):
        """
        Return page icon.
        """
        return self.iconController.get_icon(self)

    @icon.setter
    def icon(self, iconpath):
        """
        Set page icon.
        """
        return self.iconController.set_icon(self, iconpath)

    @property
    def tags(self):
        """
        Get the list of tags for the page (list of strings)
        """
        result = [tag.lower() for tag in self._tags]
        result.sort()
        return result

    @tags.setter
    def tags(self, tags):
        """
        Set tags for the page
        tags - list of tags (list of strings)
        """
        lowertags = [tag.lower() for tag in tags]
        # Remove duplicates
        newtagset = set(lowertags)
        newtags = list(newtagset)

        if newtagset != set(self._tags):
            if self.readonly:
                raise ReadonlyException(self)

            self._tags = newtags
            self.save()
            self.updateDateTime()
            self.root.onPageUpdate(self, change=events.PAGE_UPDATE_TAGS)

    def save(self):
        """
        Save the page
        """
        if self.readonly:
            return

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self._saveOptions()

    def _saveOptions(self):
        """
        Save settings
        """
        # Type
        self._params.typeOption.value = self.getTypeString()
        self._params.tagsOption.value = self._tags
        self._params.orderOption.value = self.order

    def initAfterCreating(self, tags):
        """
        Initialization after creation
        """
        self._tags = tags[:]
        self.save()
        self.creationdatetime = datetime.datetime.now()
        self.updateDateTime()
        self.parent.saveChildrenParams()
        self.root.onPageCreate(self)

    @property
    def content(self):
        """
        Read the page content file
        """
        text = ""
        path = os.path.join(self.path, PAGE_CONTENT_FILE)

        if os.path.exists(path):
            try:
                text = readTextFile(path)
                text = text.replace("\r\n", "\n")
            except Exception as e:
                logger.error("Can't read page content for %s", path)
                logger.error(str(e))

        params = events.PostContentReadingParams(text)
        self.root.onPostContentReading(self, params)
        text = params.content

        return text

    @content.setter
    def content(self, text):
        if self.readonly:
            raise ReadonlyException(self)

        text = text.replace("\r\n", "\n")

        params = events.PreContentWritingParams(text)
        self.root.onPreContentWriting(self, params)
        text = params.content

        if text != self.content or text == "":
            path = os.path.join(self.path, PAGE_CONTENT_FILE)

            writeTextFile(path, text)
            self.updateDateTime()
            self.root.onPageUpdate(self, change=events.PAGE_UPDATE_CONTENT)

    @property
    def textContent(self):
        """
        Get content in text form.
        Used for searching through pages.
        In most cases, it's enough to return just content
        """
        return self.content

    @property
    def subpath(self):
        result = self.title
        page = self.parent

        while page.parent is not None:
            # Until we reach the root, which has no title and parent is None
            result = page.title + "/" + result
            page = page.parent

        return result

    @property
    def display_subpath(self):
        result = self.display_title
        page = self.parent

        while page.parent is not None:
            result = page.display_title + "/" + result
            page = page.parent

        return result

    def remove(self):
        """
        Delete the page
        """
        if self.readonly:
            raise ReadonlyException(self)

        oldpath = self.path
        tempname = self._getTempName(oldpath)
        oldSelectedPage = self.root.selectedPage

        try:
            os.renames(oldpath, tempname)
            shutil.rmtree(tempname)
        except (OSError, shutil.Error):
            raise IOError

        self.root.onStartTreeUpdate(self.root)
        self._removePageFromTree(self)

        # If the selected page was deleted
        if oldSelectedPage is not None and (
            oldSelectedPage == self or self.isChild(oldSelectedPage)
        ):
            # New selected page instead of the old one
            newselpage = oldSelectedPage
            while newselpage.parent is not None and newselpage.isRemoved:
                newselpage = newselpage.parent

            # If we ended up at the tree root
            if newselpage.parent is None:
                newselpage = None

            self.root.selectedPage = newselpage

        self.root.onEndTreeUpdate(self.root)

    def _removePageFromTree(self, page):
        page.root.registry.remove_page_section(page)
        page.parent.removeFromChildren(page)

        for child in page.children:
            page._removePageFromTree(child)

        self.root.onPageRemove(page)

    @property
    def isRemoved(self):
        """
        Check that the page is deleted
        """
        return self not in self.parent.children

    def getUid(self, generate: bool = False) -> Optional[str]:
        uid = None
        if self._uid:
            uid = self._uid
        elif generate:
            depot = self.root.pageUidDepot
            uid = depot.generateUid()
            self.setUid(uid)
        return uid

    def setUid(self, new_uid: str) -> None:
        if self.readonly:
            raise ReadonlyException

        if new_uid is None or len(new_uid.strip()) == 0:
            raise ValueError

        new_uid = new_uid.lower()

        oldUid = self._uid
        if new_uid == oldUid:
            return

        depot = self.root.pageUidDepot
        if depot.uidExists(new_uid):
            raise KeyError

        # Prohibited to use "/" in the identifier
        if "/" in new_uid:
            raise ValueError

        depot.removePageUid(oldUid)

        self._uid = new_uid
        self.params.pageUidOption.value = new_uid
        self.updateDateTime()
        depot.addPage(self)
        self.root.onPageUpdate(self, change=events.PAGE_UPDATE_UID)

    def _clearUid(self):
        """Remove page UID. Used in tests"""
        depot = self.root.pageUidDepot
        depot.removePageUid(self._uid)
        self._uid = None
        self.params.pageUidOption.value = None


class PageAdapter:
    def __init__(self, page: WikiPage) -> None:
        self._page = page

    @property
    def page(self):
        return self._page

    def getTypeString(self) -> Optional[str]:
        return self._page.getTypeString()

    @property
    def params(self) -> PageConfig:
        return self._page.params

    @property
    def path(self) -> str:
        return self._page.path

    @property
    def parent(self) -> Optional[BasePage]:
        return self._page.parent

    @property
    def children(self) -> List[WikiPage]:
        return self._page.children

    @children.setter
    def children(self, children: List[WikiPage]):
        self._page.children = children

    @property
    def root(self) -> BasePage:
        return self._page.root

    def save(self):
        self._page.save()

    def __len__(self) -> int:
        return len(self._page)

    def __getitem__(self, path: str) -> Optional[Union[BasePage, WikiPage]]:
        return self._page[path]

    def sortChildren(
        self, key_func: Callable[["WikiPage"], Any], reverse: bool = False
    ):
        self._page.sortChildren(key_func, reverse)

    def changeChildOrder(self, page, neworder):
        self._page.changeChildOrder(page, neworder)

    def saveChildrenParams(self):
        self._page.saveChildrenParams()

    def addToChildren(self, page, order):
        self._page.addToChildren(page, order)

    def removeFromChildren(self, page):
        self._page.removeFromChildren(page)

    def isChild(self, page):
        return self._page.isChild(page)

    @property
    def datetime(self):
        return self._page.datetime

    @datetime.setter
    def datetime(self, date):
        self._page.datetime = date

    @property
    def creationdatetime(self):
        return self._page.creationdatetime

    @creationdatetime.setter
    def creationdatetime(self, date):
        self._page.creationdatetime = date

    def updateDateTime(self):
        self._page.updateDateTime()

    def update(self):
        self._page.update()

    @property
    def currentAttachSubdir(self) -> str:
        return self._page.currentAttachSubdir

    @currentAttachSubdir.setter
    def currentAttachSubdir(self, value: str):
        self._page.currentAttachSubdir = value

    def isCurrentAttachSubdirRoot(self):
        return self._page.isCurrentAttachSubdirRoot()

    @property
    def order(self):
        return self._page.order

    @order.setter
    def order(self, neworder):
        self._page.order = neworder

    @property
    def alias(self):
        return self._page.alias

    @alias.setter
    def alias(self, value):
        self._page.alias = value

    @property
    def display_title(self):
        return self._page.display_title

    @display_title.setter
    def display_title(self, value):
        self._page.display_title = value

    @property
    def title(self):
        return self._page.title

    @title.setter
    def title(self, newtitle):
        self._page.title = newtitle

    def canRename(self, newtitle):
        return self._page.canRename(newtitle)

    def moveTo(self, newparent):
        self._page.moveTo(newparent)

    @property
    def icon(self):
        return self._page.icon

    @icon.setter
    def icon(self, iconpath):
        self._page.icon = iconpath

    @property
    def tags(self):
        return self._page.tags

    @tags.setter
    def tags(self, tags):
        self._page.tags = tags

    @property
    def content(self):
        return self._page.content

    @content.setter
    def content(self, text):
        self._page.content = text

    @property
    def textContent(self):
        return self._page.textContent

    @property
    def subpath(self):
        return self._page.subpath

    @property
    def display_subpath(self):
        return self._page.display_subpath

    def remove(self):
        self._page.remove()

    @property
    def isRemoved(self):
        return self._page.isRemoved

    @property
    def readonly(self):
        return self._page.readonly


class PageUidDepot:
    """
    Class for storing unique page identifiers and references to them
    """

    def __init__(self):
        """
        wikiroot - wiki tree root or root page.
        If wikiroot != None, then all UIDs are searched
        """
        # Dictionary of identifiers.
        # Key - unique identifier, value - pointer to page
        self.__uids: Dict[str, BasePage] = {}

    def load(self, wikiroot: Optional[WikiDocument]) -> None:
        self.__uids.clear()

        if wikiroot is not None:
            self.__load(wikiroot)

    def __load(self, root: BasePage):
        """
        Read UID of all pages in the tree.
        """
        uid = root.getUid(generate=False)

        if uid is not None:
            self.__uids[uid] = root

        [self.__load(child) for child in root.children]

    def __getitem__(self, uid: str) -> Optional[BasePage]:
        uid = uid.lower()

        page = self.__uids.get(uid, None)

        if page is not None and page.getTypeString() != "document" and page.isRemoved:
            del self.__uids[uid]
            page = None

        return page

    def generateUid(self) -> str:
        while (uid := str(uuid.uuid4())) in self.__uids:
            pass

        return uid

    def removePageUid(self, uid: Optional[str]) -> None:
        if uid in self.__uids:
            del self.__uids[uid]

    def addPage(self, page: BasePage) -> None:
        uid = page.getUid(generate=False)
        assert uid is not None
        self.__uids[uid] = page

    def uidExists(self, uid: str) -> bool:
        return uid in self.__uids

# coding: utf-8

import logging
import os
from typing import Optional

import wx

from outwiker.core.defines import ICON_HEIGHT
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.imagelistcache import ImageListCache

logger = logging.getLogger("outwiker.gui.controls.notestreectrl")


class NotesTreeCtrl2(wx.Control):
    def __init__(self, parent: wx.Window):
        super().__init__(parent)

        self.defaultIcon = getBuiltinImagePath('page.svg')
        self.iconHeight = ICON_HEIGHT

        # Картинки для дерева
        self._iconsCache = ImageListCache(self.defaultIcon)
        # self.AssignImageList(self._iconsCache.getImageList())

        # Кеш для страниц, чтобы было проще искать элемент дерева по странице
        # Словарь. Ключ - страница, значение - элемент дерева wx.TreeItemId
        self._pageCache = {}

        # Имя опции для сохранения развернутости страницы
        self.pageOptionExpand = 'Expand'

        self.Bind(wx.EVT_CLOSE, self._onClose)

    def _onClose(self, event):
        self._iconsCache.clear()

    def _addRoot(self, title, data, imageId: int):
        pass

    def _deleteAllItems(self):
        pass

    def treeUpdate(self, rootPage):
        """
        Обновить дерево
        """
        self._deleteAllItems()
        self._iconsCache.clear()

        # Ключ - страница, значение - экземпляр класса TreeItemId
        self._pageCache = {}

        if rootPage is not None:
            rootname = os.path.basename(rootPage.path)
            rootItem = self._addRoot(
                rootname,
                data=rootPage,
                imageId=self._iconsCache.getDefaultImageId())

            self._pageCache[rootPage] = rootItem
            self.appendChildren(rootPage)

            self.selectedPage = rootPage.selectedPage
            self.expand(rootPage)

    def appendChildren(self, parentPage):
        """
        Добавить детей в дерево
        parentPage - родительская страница, куда добавляем дочерние страницы
        """
        # grandParentExpanded = self._getItemExpandState(parentPage.parent)

        # if grandParentExpanded:
        #     for child in parentPage.children:
        #         if child not in self._pageCache:
        #             self.insertChild(child)

        # if self._getPageExpandState(parentPage):
        #     self.expand(parentPage)

    def insertChild(self, childPage):
        """
        Вставить одну дочерниюю страницу (childPage) в ветвь
        """
        # parentItem = self.getTreeItem(childPage.parent)
        # assert parentItem is not None

        # item = self.InsertItem(parentItem,
        #                        childPage.order,
        #                        childPage.display_title,
        #                        data=childPage)

        # self.SetItemImage(item, self._loadIcon(childPage))

        # self._pageCache[childPage] = item
        # self._mountItem(item, childPage)
        # self.appendChildren(childPage)

        # return item

    def removePageItem(self, page):
        """
        Удалить элемент, соответствующий странице и все его дочерние страницы
        """
        # for child in page.children:
        #     self.removePageItem(child)

        # item = self.getTreeItem(page)
        # if item is not None:
        #     del self._pageCache[page]
        #     self.Delete(item)

    def _loadIcon(self, page):
        """
        Добавляет иконку страницы в ImageList и возвращает ее идентификатор.
        Если иконки нет, то возвращает идентификатор иконки по умолчанию
        """
        icon = page.icon

        if not icon:
            return self._iconsCache.getDefaultImageId()

        icon = os.path.abspath(icon)
        page_path = os.path.abspath(page.path)

        try:
            if icon.startswith(page_path):
                imageId = self._iconsCache.replace(icon)
            else:
                imageId = self._iconsCache.add(icon)
        except Exception:
            logger.error("Invalid icon file: %s", icon)
            imageId = self._iconsCache.getDefaultImageId()
        return imageId

    def updateIcon(self, page):
        # if page not in self._pageCache:
        #     # Если нет этой страницы в дереве, то не важно,
        #     # изменилась иконка или нет
        #     return

        # icon_id = self._loadIcon(page)
        # self.SetItemImage(self._pageCache[page], icon_id)
        pass

    # def _getItemExpandState(self, page):
    #     """
    #     Проверить, раскрыт ли элемент в дереве для страницы page
    #     """
    #     if page is None:
    #         return True

    #     if page.parent is None:
    #         return True

    #     return self.IsExpanded(self._pageCache[page])

    # def _getPageExpandState(self, page):
    #     """
    #     Проверить состояние "раскрытости" страницы
    #     """
    #     if page is None:
    #         return True

    #     if page.parent is None:
    #         return True

    #     page_registry = page.root.registry.get_page_registry(page)
    #     expanded = page_registry.getbool(self.pageOptionExpand, default=False)

    #     return expanded

    def getTreeItem(self, page: 'outwiker.core.tree.WikiPage') -> Optional[wx.TreeItemId]:
        """
        Получить элемент дерева по странице.
        Если для страницы не создан элемент дерева, возвращается None
        """
        return self._pageCache.get(page)

    def expandToPage(self, page):
        """
        Развернуть ветви до того уровня, чтобы появился элемент для page
        """
        # Список родительских страниц, которые нужно добавить в дерево
        # pages = []
        # currentPage = page.parent
        # while currentPage is not None:
        #     pages.append(currentPage)
        #     currentPage = currentPage.parent

        # pages.reverse()
        # for page in pages:
        #     self.expand(page)

    def expand(self, page):
        # item = self.getTreeItem(page)
        # if item is not None:
        #     self.Expand(item)
        pass

    def createPage(self, newpage):
        # if newpage.parent in self._pageCache:
        #     self.insertChild(newpage)

        #     assert newpage in self._pageCache
        #     item = self._pageCache[newpage]
        #     assert item.IsOk()

        #     self.expand(newpage)
        pass

    @property
    def selectedPage(self):
        page = None

        # item = self.GetSelection()
        # if item.IsOk():
        #     page = self.GetItemData(item)

        #     # Проверка того, что выбрали не корневой элемент
        #     if page.parent is None:
        #         page = None

        return page

    @selectedPage.setter
    def selectedPage(self, newSelPage):
        # if newSelPage is None:
        #     item = self.GetRootItem()
        # else:
        #     self.expandToPage(newSelPage)
        #     item = self.getTreeItem(newSelPage)

        # if item is not None:
        #     self.SelectItem(item)
        pass

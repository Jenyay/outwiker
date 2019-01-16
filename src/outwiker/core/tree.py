# -*- coding: utf-8 -*-

import logging
import os
import os.path
import configparser
import shutil
import datetime
from functools import cmp_to_key
from functools import reduce

from .config import PageConfig
from .bookmarks import Bookmarks
from .event import Event
from .exceptions import (ClearConfigError, RootFormatError, DuplicateTitle,
                         ReadonlyException, TreeException)
from .tagscommands import parseTagsList
from .sortfunctions import sortOrderFunction, sortAlphabeticalFunction
from .defines import PAGE_CONTENT_FILE, PAGE_OPT_FILE, REGISTRY_FILE
from .iconcontroller import IconController
from .system import getIconsDirList
from .registrynotestree import NotesTreeRegistry, PickleSaver
from . import events
from outwiker.utilites.textfile import readTextFile, writeTextFile


logger = logging.getLogger('core')


class RootWikiPage(object):
    """
    Класс для корня вики
    """
    contentFile = PAGE_CONTENT_FILE

    sectionGeneral = u"General"

    def __init__(self, path, readonly=False):
        """
        readonly - True, если страница предназначена только для чтения
        """
        # Путь до страницы
        self._path = path
        self._parent = None
        self._children = []
        self.readonly = readonly

        configpath = os.path.join(path, PAGE_OPT_FILE)
        if (not self.readonly and
                os.path.exists(configpath) and
                not os.access(configpath, os.W_OK)):
            self.readonly = True

        self._params = RootWikiPage._readParams(self.path, self.readonly)
        self._datetime = self._getDateTime()

    @staticmethod
    def _readParams(path, readonly=False):
        return PageConfig(os.path.join(path, PAGE_OPT_FILE), readonly)

    @property
    def params(self):
        return self._params

    @property
    def path(self):
        return self._path

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children[:]

    @property
    def root(self):
        """
        Найти корень дерева по странице
        """
        result = self
        while result.parent is not None:
            result = result.parent

        return result

    def save(self):
        if self.readonly:
            return

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self._params.save()

    def __len__(self):
        return len(self._children)

    def __getitem__(self, path):
        """
        Получить нужную страницу по относительному пути в дереве
        """
        if len(path) == 0:
            return None

        if path == "/":
            return self.root

        # Если путь начинается с "/", то отсчет начнем от корня
        if path[0] == "/":
            return self.root[path[1:]]

        # Разделим путь по составным частям
        titles = path.split("/")
        page = self

        for title in titles:
            found = False
            if title == u"..":
                page = page.parent
                found = (page is not None)
            else:
                for child in page.children:
                    if child.title.lower() == title.lower():
                        page = child
                        found = True

            if not found:
                page = None
                break

        return page

    def sortChildrenAlphabetical(self):
        """
        Отсортировать дочерние страницы по алфавиту
        """
        self._children.sort(key=cmp_to_key(sortAlphabeticalFunction))

        self.root.onStartTreeUpdate(self.root)
        self.saveChildrenParams()
        self.root.onEndTreeUpdate(self.root)

    @staticmethod
    def testDublicate(parent, title):
        """
        Проверить заголовок страницы на то, что в родителе нет
        страницы с таким заголовком
        """
        return parent[title] is None

    def _changeChildOrder(self, page, neworder):
        """
        Изменить порядок дочерних элементов
        Дочернюю страницу page переместить на уровень neworder
        """
        oldorder = self._children.index(page)
        if oldorder != neworder:
            self.removeFromChildren(page)
            self._children.insert(neworder, page)
            self.saveChildrenParams()

    def saveChildrenParams(self):
        for child in self._children:
            child.save()

    def addToChildren(self, page):
        """
        Добавить страницу к дочерним страницам
        """
        self._children.append(page)
        self._children.sort(key=cmp_to_key(sortOrderFunction))

    def removeFromChildren(self, page):
        """
        Удалить страницу из дочерних страниц
        """
        self._children.remove(page)

    def isChild(self, page):
        """
        Проверить, является ли page дочерней(вложенной) страницей для self
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
        Получить дату и время изменения страницы в виде экземпляра
        класса datetime.datetime
        """
        return self._datetime

    def _getDateTime(self):
        date = self.params.datetimeOption.value
        if date is None:
            # Если дата не установлена, то возвратим дату последнего
            # изменения файла с контентом, при этом запишем эту дату в
            # файл настроек
            contentpath = os.path.join(self.path, RootWikiPage.contentFile)
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
        Установить дату изменения страницы в текущую дату/время
        """
        self.datetime = datetime.datetime.now()

    def update(self):
        '''
        Update page content if needed.
        The method can raise EnvironmentError.
        '''
        pass

    def loadChildren(self):
        """
        Загрузить дочерние узлы
        """
        try:
            entries = os.listdir(self.path)
        except OSError:
            raise IOError

        self._children = []

        for name in entries:
            fullpath = os.path.join(self.path, name)

            if not name.startswith("__") and os.path.isdir(fullpath):
                try:
                    page = WikiPage.load(fullpath, self, self.root.readonly)
                except Exception as e:
                    text = 'Error reading page {}'.format(fullpath)
                    logging.error(text)
                    logging.error(u'    ' + str(e))
                    continue

                self._children.append(page)

        self._children.sort(key=cmp_to_key(sortOrderFunction))


class WikiDocument(RootWikiPage):
    def __init__(self, path, readonly=False):
        RootWikiPage.__init__(self, path, readonly)
        self._selectedPage = None
        self._createEvents()
        self.bookmarks = Bookmarks(self, self._params)
        self._registry = NotesTreeRegistry(self._getRegistrySaver(self._path))

    def _getRegistrySaver(self, path):
        registry_path = os.path.join(path, REGISTRY_FILE)
        return PickleSaver(registry_path)

    def _createEvents(self):
        # Выбор новой страницы
        # Параметры: новая выбранная страница
        self.onPageSelect = Event()

        # Обновление дерева
        # Параметры: sender - из-за кого обновляется дерево
        self.onTreeUpdate = Event()

        # Начало сложного обновления дерева
        # Параметры: root - корень дерева
        self.onStartTreeUpdate = Event()

        # Конец сложного обновления дерева
        # Параметры: root - корень дерева
        self.onEndTreeUpdate = Event()

        # Обновление страницы
        # Параметры:
        #     sender
        #     **kwargs
        # kwargs содержит значение 'change', хранящее флаги того,
        #     что изменилось
        self.onPageUpdate = Event()

        # Изменение порядка страниц
        # Параметры: page - страница, положение которой изменили
        self.onPageOrderChange = Event()

        # Переименование страницы.
        # Параметры:
        #   page - переименованная страница,
        #   oldSubpath - старый относительный путь до страницы
        self.onPageRename = Event()

        # Создание страницы
        # Параметры: sender
        self.onPageCreate = Event()

        # Удаленеи страницы
        # Параметр - удаленная страница
        self.onPageRemove = Event()

        # Event occurs after change attached file list.
        # Parameters:
        #     page - current (selected) page
        #     params - instance if the AttachListChangedParams class
        self.onAttachListChanged = Event()

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

    @staticmethod
    def clearConfigFile(path):
        """
        Очистить файл __page.opt.
        Используется в случае, если файл __page.opt испорчен
        path - путь до вики(или до директории с файлом __page.opt,
        или включая этот файл)
        """
        if path.endswith(PAGE_OPT_FILE):
            realpath = path
        else:
            realpath = os.path.join(path, PAGE_OPT_FILE)

        try:
            fp = open(realpath, "w", encoding='utf8')
            fp.close()
        except IOError:
            raise ClearConfigError

    @staticmethod
    def load(path, readonly=False):
        """
        Загрузить корневую страницу вики.
        Использовать этот метод вместо конструктора
        """
        try:
            root = WikiDocument(path, readonly)
        except configparser.Error:
            raise RootFormatError

        root.loadChildren()

        root.onTreeUpdate(root)
        return root

    def save(self):
        super().save()
        self._registry.save()

    @staticmethod
    def create(path):
        """
        Создать корень для вики
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
        if isinstance(page, type(self)) or page is None:
            # Экземпляр класса WikiDocument выбирать нельзя
            self._selectedPage = None
        else:
            self._selectedPage = page

        self.root.onPageSelect(self._selectedPage)
        self.save()

    @property
    def subpath(self):
        return u"/"

    @property
    def display_subpath(self):
        return u"/"

    @property
    def title(self):
        return os.path.basename(self.path)

    @staticmethod
    def getTypeString():
        return u"document"

    @property
    def registry(self):
        return self._registry


class WikiPage(RootWikiPage):
    """
    Страница в дереве.
    """
    paramTags = u"tags"
    paramType = u"type"

    iconController = IconController(getIconsDirList()[0])

    @staticmethod
    def getTypeString():
        return u"base"

    def __init__(self, path, title, parent, readonly=False):
        """
        Constructor.

        path -- путь до страницы
        """
        if not RootWikiPage.testDublicate(parent, title):
            logger.error(u'Duplicate page title in the parent page. Title: {}. Parent: {}'.format(title, parent.subpath))
            raise DuplicateTitle

        RootWikiPage.__init__(self, path, readonly)
        self._title = title
        self._parent = parent
        self._alias = self.params.aliasOption.value
        if len(self._alias) == 0:
            self._alias = None

    @property
    def order(self):
        """
        Вернуть индекс страницы в списке дочерних страниц
        """
        return self.parent.children.index(self)

    @order.setter
    def order(self, neworder):
        """
        Изменить положение страницы(порядок)
        """
        if self.readonly:
            raise ReadonlyException

        realorder = neworder

        if realorder < 0:
            realorder = 0

        if realorder >= len(self.parent.children):
            realorder = len(self.parent.children) - 1

        self.parent._changeChildOrder(self, realorder)
        self.root.onPageOrderChange(self)

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value):
        if self.readonly:
            raise ReadonlyException

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
        if self.readonly:
            raise ReadonlyException

        oldtitle = self.title
        oldpath = self.path
        oldsubpath = self.subpath

        if oldtitle == newtitle:
            return

        # Проверка на дубликат страниц, а также на то, что в заголовке страницы
        # может меняться только регистр букв
        if not self.canRename(newtitle):
            raise DuplicateTitle

        newpath = os.path.join(os.path.dirname(oldpath), newtitle)
        os.renames(oldpath, newpath)
        self._title = newtitle

        WikiPage._renamePaths(self, newpath)
        self.root.registry.rename_page_sections(oldsubpath, self.subpath)

        self.root.onPageRename(self, oldsubpath)
        self.root.onPageUpdate(self, change=events.PAGE_UPDATE_TITLE)

    def canRename(self, newtitle):
        return (self.title.lower() == newtitle.lower() or
                self.parent[newtitle] is None)

    @staticmethod
    def _renamePaths(page, newPath):
        """
        Скорректировать пути после переименования страницы
        """
        oldPath = page.path
        page._path = newPath
        page._params = RootWikiPage._readParams(page.path)

        for child in page.children:
            newChildPath = child.path.replace(oldPath, newPath, 1)
            WikiPage._renamePaths(child, newChildPath)

    def moveTo(self, newparent):
        """
        Переместить запись к другому родителю
        """
        if self.readonly or newparent.readonly:
            raise ReadonlyException

        if self._parent == newparent:
            return

        if self.isChild(newparent):
            # Нельзя быть родителем своего родителя(предка)
            raise TreeException

        # Проверка на то, что в новом родителе нет записи с таким же заголовком
        if newparent[self.title] is not None:
            raise DuplicateTitle

        oldpath = self.path
        oldparent = self.parent
        oldsubpath = self.subpath

        # Новый путь для страницы
        newpath = os.path.join(newparent.path, self.title)

        # Временное имя папки.
        # Сначала попробуем переименовать папку во временную,
        # а потом уже ее переместим в нужное место с нужным именем
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
        newparent.addToChildren(self)

        newsubpath = self.subpath
        WikiPage._renamePaths(self, newpath)
        self.root.registry.rename_page_sections(oldsubpath, newsubpath)

        self.root.onTreeUpdate(self)

    def _getTempName(self, pagepath):
        """
        Найти уникальное имя для перемещаемой страницы.
        При перемещении сначала пробуем переименовать папку со страницей,
        а потом уже перемещать.

        pagepath - текущий путь до страницы

        Метод возвращает полный путь
        """
        path, title = os.path.split(pagepath)
        template = u"__{title}_{number}"
        number = 0
        newname = template.format(title=title, number=number)

        while os.path.exists(os.path.join(path, newname)):
            number += 1
            newname = template.format(title=title, number=number)

        return os.path.join(path, newname)

    @property
    def icon(self):
        '''
        Return page icon.
        '''
        return self.iconController.get_icon(self)

    @icon.setter
    def icon(self, iconpath):
        '''
        Return page icon.
        '''
        return self.iconController.set_icon(self, iconpath)

    @property
    def tags(self):
        """
        Получить список тегов для страницы(список строк)
        """
        result = [tag.lower() for tag in self._tags]
        result.sort()
        return result

    @tags.setter
    def tags(self, tags):
        """
        Установить теги для страницы
        tags - список тегов(список строк)
        """
        if self.readonly:
            raise ReadonlyException

        lowertags = [tag.lower() for tag in tags]
        # Избавимся от дубликатов
        newtagset = set(lowertags)
        newtags = list(newtagset)

        if newtagset != set(self._tags):
            self._tags = newtags
            self.save()
            self.updateDateTime()
            self.root.onPageUpdate(self, change=events.PAGE_UPDATE_TAGS)

    @staticmethod
    def load(path, parent, readonly=False):
        """
        Загрузить страницу.
        Использовать этот метод вместо конструктора,
        когда надо загрузить страницу
        """
        from .factoryselector import FactorySelector

        title = os.path.basename(path)
        params = RootWikiPage._readParams(path, readonly)

        # Получим тип страницы по параметрам
        pageType = FactorySelector.getFactory(params.typeOption.value).getPageType()

        page = pageType(path, title, parent, readonly)
        page._tags = WikiPage.getTags(params)
        page.loadChildren()

        return page

    def save(self):
        """
        Сохранить страницу
        """
        if self.readonly:
            return

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self._saveOptions()

    def _saveOptions(self):
        """
        Сохранить настройки
        """
        # Тип
        self._params.typeOption.value = self.getTypeString()

        # Теги
        self._saveTags()

        # Порядок страницы
        self._params.orderOption.value = self.order

    def _saveTags(self):
        tags = reduce(lambda full, tag: full + ", " + tag, self._tags, "")

        # Удалим начальные ", "
        tags = tags[2:]
        self._params.set(RootWikiPage.sectionGeneral, WikiPage.paramTags, tags)

    def initAfterCreating(self, tags):
        """
        Инициализация после создания
        """
        self._tags = tags[:]
        self.save()
        self.creationdatetime = datetime.datetime.now()
        self.updateDateTime()
        self.parent.saveChildrenParams()
        self.root.onPageCreate(self)

    @staticmethod
    def getTags(configParser):
        """
        Выделить теги из строки конфигурационного файла
        """
        try:
            tagsString = configParser.get(RootWikiPage.sectionGeneral,
                                          WikiPage.paramTags)
        except configparser.NoOptionError:
            return []

        tags = parseTagsList(tagsString)

        return tags

    @property
    def content(self):
        """
        Прочитать файл-содержимое страницы
        """
        text = ""
        path = os.path.join(self.path, RootWikiPage.contentFile)

        if os.path.exists(path):
            try:
                text = readTextFile(path)
                text = text.replace('\r\n', '\n')
            except Exception as e:
                logger.error("Can't read page content for {}".format(path))
                logger.error(str(e))

        params = events.PostContentReadingParams(text)
        self.root.onPostContentReading(self, params)
        text = params.content

        return text

    @content.setter
    def content(self, text):
        if self.readonly:
            raise ReadonlyException

        text = text.replace('\r\n', '\n')

        params = events.PreContentWritingParams(text)
        self.root.onPreContentWriting(self, params)
        text = params.content

        if text != self.content or text == u"":
            path = os.path.join(self.path, RootWikiPage.contentFile)

            writeTextFile(path, text)
            self.updateDateTime()
            self.root.onPageUpdate(self, change=events.PAGE_UPDATE_CONTENT)

    @property
    def textContent(self):
        """
        Получить контент в текстовом виде.
        Используется для поиска по страницам.
        В большинстве случаев достаточно вернуть просто content
        """
        return self.content

    @property
    def subpath(self):
        result = self.title
        page = self.parent

        while page.parent is not None:
            # Пока не дойдем до корня, у которого нет заголовка,
            # и родитель - None
            result = page.title + "/" + result
            page = page.parent

        return result

    @property
    def display_subpath(self):
        '''
        Added in outwiker.core 1.3
        '''
        result = self.display_title
        page = self.parent

        while page.parent is not None:
            result = page.display_title + "/" + result
            page = page.parent

        return result

    def remove(self):
        """
        Удалить страницу
        """
        if self.readonly:
            raise ReadonlyException

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

        # Если выбранная страница была удалена
        if (oldSelectedPage is not None and
                (oldSelectedPage == self or self.isChild(oldSelectedPage))):
            # Новая выбранная страница взамен старой
            newselpage = oldSelectedPage
            while newselpage.parent is not None and newselpage.isRemoved:
                newselpage = newselpage.parent

            # Если попали в корень дерева
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
        Проверить, что страница удалена
        """
        return self not in self.parent.children

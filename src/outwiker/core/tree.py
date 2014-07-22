# -*- coding: UTF-8 -*-

import os
import os.path
import ConfigParser
import shutil
import datetime

from .config import PageConfig
from .bookmarks import Bookmarks
from .event import Event
from .exceptions import ClearConfigError, RootFormatError, DublicateTitle, ReadonlyException, TreeException
from .tagscommands import parseTagsList
from .sortfunctions import sortOrderFunction, sortAlphabeticalFunction
import events


class RootWikiPage (object):
    """
    Класс для корня вики
    """
    pageConfig = u"__page.opt"
    contentFile = u"__page.text"
    iconName = u"__icon"

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

        configpath = os.path.join (path, RootWikiPage.pageConfig)
        if (not self.readonly and
                os.path.exists (configpath) and
                not os.access (configpath, os.W_OK)):
            self.readonly = True

        self._params = RootWikiPage._readParams(self.path, self.readonly)


    @staticmethod
    def _readParams (path, readonly=False):
        return PageConfig (os.path.join (path, RootWikiPage.pageConfig), readonly)


    @property
    def params (self):
        return self._params


    @property
    def path (self):
        return self._path


    @property
    def parent (self):
        return self._parent


    @property
    def children (self):
        return self._children[:]


    @property
    def root (self):
        """
        Найти корень дерева по странице
        """
        result = self
        while result.parent is not None:
            result = result.parent

        return result


    def save (self):
        if self.readonly:
            return

        if not os.path.exists (self.path):
            os.mkdir (self.path)

        self._params.save()


    def __len__ (self):
        return len (self._children)


    def __getitem__ (self, path):
        """
        Получить нужную страницу по относительному пути в дереве
        """
        if len (path) == 0:
            return None

        if path == "/":
            return self.root

        # Если путь начинается с "/", то отсчет начнем от корня
        if path[0] == "/":
            return self.root[path[1:]]

        # Разделим путь по составным частям
        titles = path.split ("/")
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


    def getChildren(self):
        """
        Загрузить дочерние узлы
        """
        try:
            entries = os.listdir (self.path)
        except OSError:
            raise IOError

        result = []

        for name in entries:
            fullpath = os.path.join (self.path, name)

            if not name.startswith ("__") and os.path.isdir (fullpath):
                try:
                    page = WikiPage.load (fullpath, self, self.root.readonly)
                except Exception:
                    continue

                result.append (page)

        result.sort (sortOrderFunction)

        return result


    def sortChildrenAlphabetical(self):
        """
        Отсортировать дочерние страницы по алфавиту
        """
        self._children.sort (sortAlphabeticalFunction)

        self.root.onStartTreeUpdate (self.root)
        self.saveChildrenParams()
        self.root.onEndTreeUpdate (self.root)



    @staticmethod
    def testDublicate (parent, title):
        """
        Проверить заголовок страницы на то, что в родителе нет страницы с таким заголовком
        """
        return parent[title] is None


    def _changeChildOrder (self, page, neworder):
        """
        Изменить порядок дочерних элементов
        Дочернюю страницу page переместить на уровень neworder
        """
        oldorder = self._children.index (page)
        if oldorder != neworder:
            self.removeFromChildren (page)
            self._children.insert (neworder, page)
            self.saveChildrenParams()


    def saveChildrenParams (self):
        for child in self._children:
            child.save()


    def addToChildren (self, page):
        """
        Добавить страницу к дочерним страницам
        """
        self._children.append (page)
        self._children.sort (sortOrderFunction)


    def removeFromChildren (self, page):
        """
        Удалить страницу из дочерних страниц
        """
        self._children.remove (page)


    def isChild (self, page):
        """
        Проверить, является ли page дочерней (вложенной) страницей для self
        """
        currentpage = page
        while currentpage is not None:
            if currentpage == self:
                return True
            currentpage = currentpage.parent

        return False


    @property
    def datetime (self):
        """
        Получить дату и время изменения страницы в виде экземпляра класса datetime.datetime
        """
        date = self.params.datetimeOption.value
        if date is None:
            # Если дата не установлена, то возвратим дату последнего изменения файла с контентом,
            # при этом запишем эту дату в файл настроек
            contentpath = os.path.join (self.path, RootWikiPage.contentFile)
            if os.path.exists (contentpath):
                time = os.path.getmtime(contentpath)
                date = datetime.datetime.fromtimestamp(time)
                self.datetime = date

        return date


    @datetime.setter
    def datetime (self, date):
        self.params.datetimeOption.value = date


    @property
    def creationdatetime (self):
        date = self.params.creationDatetimeOption.value
        if date is None:
            date = self.datetime
            self.creationdatetime = date

        return date


    @creationdatetime.setter
    def creationdatetime (self, date):
        self.params.creationDatetimeOption.value = date


    def updateDateTime (self):
        """
        Установить дату изменения страницы в текущую дату/время
        """
        self.datetime = datetime.datetime.now()


class WikiDocument (RootWikiPage):
    def __init__ (self, path, readonly = False):
        RootWikiPage.__init__ (self, path, readonly)
        self._selectedPage = None
        self.__createEvents()
        self.bookmarks = Bookmarks (self, self._params)


    def __createEvents (self):
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
        # kwargs содержит значение 'change', хранящее флаги того, что изменилось
        self.onPageUpdate = Event()

        # Изменение порядка страниц
        # Параметры: page - страница, положение которой изменили
        self.onPageOrderChange = Event()

        # Переименование страницы.
        # Параметры: page - переименованная страница, oldSubpath - старый относительный путь до страницы
        self.onPageRename = Event()

        # Создание страницы
        # Параметры: sender
        self.onPageCreate = Event()

        # Удаленеи страницы
        # Параметр - удаленная страница
        self.onPageRemove = Event()


    @staticmethod
    def clearConfigFile (path):
        """
        Очистить файл __page.opt.
        Используется в случае, если файл __page.opt испорчен
        path - путь до вики (или до директории с файлом __page.opt, или включая этот файл)
        """
        if path.endswith (RootWikiPage.pageConfig):
            realpath = path
        else:
            realpath = os.path.join (path, RootWikiPage.pageConfig)

        try:
            fp = open (realpath, "w")
            fp.close()
        except IOError:
            raise ClearConfigError


    @staticmethod
    def load(path, readonly = False):
        """
        Загрузить корневую страницу вики.
        Использовать этот метод вместо конструктора
        """
        try:
            root = WikiDocument(path, readonly)
        except ConfigParser.Error:
            raise RootFormatError

        root.loadChildren()

        root.onTreeUpdate(root)
        return root


    def loadChildren (self):
        """
        Интерфейс для загрузки дочерних страниц
        """
        self._children = self.getChildren()


    @staticmethod
    def create (path):
        """
        Создать корень для вики
        """
        root = WikiDocument (path)
        root.save()
        root.onTreeUpdate(root)

        return root

    @property
    def selectedPage (self):
        return self._selectedPage


    @selectedPage.setter
    def selectedPage (self, page):
        if isinstance (page, type(self)) or page is None:
            # Экземпляр класса WikiDocument выбирать нельзя
            self._selectedPage = None
        else:
            self._selectedPage = page

        self.root.onPageSelect(self._selectedPage)
        self.save()


    @property
    def subpath (self):
        return u"/"


    @property
    def title (self):
        return os.path.basename (self.path)


    @staticmethod
    def getTypeString ():
        return u"document"



class WikiPage (RootWikiPage):
    """
    Страница в дереве.
    """
    paramTags = u"tags"
    paramType = u"type"

    @staticmethod
    def getTypeString ():
        return u"base"


    def __init__(self, path, title, parent, readonly = False):
        """
        Constructor.

        path -- путь до страницы
        """
        if not RootWikiPage.testDublicate(parent, title):
            raise DublicateTitle

        RootWikiPage.__init__ (self, path, readonly)
        self._title = title
        self._parent = parent


    @property
    def order (self):
        """
        Вернуть индекс страницы в списке дочерних страниц
        """
        return self.parent.children.index (self)


    @order.setter
    def order (self, neworder):
        """
        Изменить положение страницы (порядок)
        """
        if self.readonly:
            raise ReadonlyException

        realorder = neworder

        if realorder < 0:
            realorder = 0

        if realorder >= len (self.parent.children):
            realorder = len (self.parent.children) - 1

        self.parent._changeChildOrder (self, realorder)
        self.root.onPageOrderChange (self)


    @property
    def title (self):
        return self._title


    @title.setter
    def title (self, newtitle):
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
            raise DublicateTitle

        newpath = os.path.join (os.path.dirname (oldpath), newtitle)
        os.renames (oldpath, newpath)
        self._title = newtitle

        WikiPage.__renamePaths (self, newpath)

        self.root.onPageRename (self, oldsubpath)
        self.root.onTreeUpdate (self)


    def canRename (self, newtitle):
        return (self.title.lower() == newtitle.lower() or
                self.parent[newtitle] is None)


    @staticmethod
    def __renamePaths (page, newPath):
        """
        Скорректировать пути после переименования страницы
        """
        oldPath = page.path
        page._path = newPath
        page._params = RootWikiPage._readParams(page.path)

        for child in page.children:
            newChildPath = child.path.replace (oldPath, newPath, 1)
            WikiPage.__renamePaths (child, newChildPath)


    def moveTo (self, newparent):
        """
        Переместить запись к другому родителю
        """
        if self.readonly:
            raise ReadonlyException

        if self._parent == newparent:
            return

        if self.isChild (newparent):
            # Нельзя быть родителем своего родителя (предка)
            raise TreeException

        # Проверка на то, что в новом родителе нет записи с таким же заголовком
        if newparent[self.title] is not None:
            raise DublicateTitle

        oldpath = self.path
        oldparent = self.parent

        # Новый путь для страницы
        newpath = os.path.join (newparent.path, self.title)

        # Временное имя папки.
        # Сначала попробуем переименовать папку во временную,
        # а потом уже ее переместим в нужное место с нужным именем
        tempname = self._getTempName (oldpath)

        try:
            os.renames (oldpath, tempname)
            shutil.move (tempname, newpath)
        except shutil.Error:
            raise TreeException
        except OSError:
            raise TreeException

        self._parent = newparent
        oldparent.removeFromChildren (self)
        newparent.addToChildren (self)

        WikiPage.__renamePaths (self, newpath)

        self.root.onTreeUpdate (self)


    def _getTempName (self, pagepath):
        """
        Найти уникальное имя для перемещаемой страницы.
        При перемещении сначала пробуем переименовать папку со страницей, а потом уже перемещать
        pagepath - текущий путь до страницы

        Метод возвращает полный путь
        """
        (path, title) = os.path.split (pagepath)
        template = u"__{title}_{number}"
        number = 0
        newname = template.format (title=title, number=number)

        while (os.path.exists (os.path.join (path, newname))):
            number += 1
            newname = template.format (title=title, number=number)

        return os.path.join (path, newname)


    @property
    def icon (self):
        icons = self._getIconFiles()
        return icons[0] if len (icons) > 0 else None


    @icon.setter
    def icon (self, iconpath):
        if self.readonly:
            raise ReadonlyException

        if self.icon is not None and os.path.abspath (self.icon) == os.path.abspath (iconpath):
            return

        self._removeOldIcons()

        name = os.path.basename (iconpath)
        dot = name.rfind (".")
        extension = name[dot:]

        newname = RootWikiPage.iconName + extension
        newpath = os.path.join (self.path, newname)

        if iconpath != newpath:
            shutil.copyfile (iconpath, newpath)
            self.updateDateTime()

        self.root.onPageUpdate (self, change=events.PAGE_UPDATE_ICON)

        return newpath


    def _removeOldIcons (self):
        for fname in self._getIconFiles():
            os.remove (fname)


    @property
    def tags (self):
        """
        Получить список тегов для страницы (список строк)
        """
        result = [tag.lower() for tag in self._tags]
        result.sort()
        return result


    @tags.setter
    def tags (self, tags):
        """
        Установить теги для страницы
        tags - список тегов (список строк)
        """
        if self.readonly:
            raise ReadonlyException

        lowertags = [tag.lower() for tag in tags]
        # Избавимся от дубликатов
        newtagset = set (lowertags)
        newtags = list (newtagset)

        if newtagset != set (self._tags):
            self._tags = newtags
            self.save()
            self.updateDateTime()
            self.root.onPageUpdate(self, change=events.PAGE_UPDATE_TAGS)


    def _getIconFiles (self):
        files = os.listdir (self.path)

        icons = [os.path.join (self.path, fname) for fname in files
                 if (fname.startswith (RootWikiPage.iconName) and
                     not os.path.isdir (fname))]

        return icons


    def initAfterLoading (self):
        """
        Инициализировать после загрузки (загрузить параметры страницы)
        """
        # Теги страницы
        self._tags = self._getTags (self._params)

        self._children = self.getChildren ()


    @staticmethod
    def load (path, parent, readonly = False):
        """
        Загрузить страницу.
        Использовать этот метод вместо конструктора, когда надо загрузить страницу
        """
        from .factoryselector import FactorySelector

        title = os.path.basename(path)
        params = RootWikiPage._readParams(path, readonly)

        # Получим тип страницы по параметрам
        pageType = FactorySelector.getFactory(params.typeOption.value).getPageType()

        page = pageType (path, title, parent, readonly)
        page.initAfterLoading ()

        return page


    def save (self):
        """
        Сохранить страницу
        """
        if self.readonly:
            return

        if not os.path.exists (self.path):
            os.mkdir (self.path)

        self._saveOptions ()


    def _saveOptions (self):
        """
        Сохранить настройки
        """
        # Тип
        self._params.typeOption.value = self.getTypeString()

        # Теги
        self._saveTags()

        # Порядок страницы
        self._params.orderOption.value = self.order


    def _saveTags (self):
        tags = reduce (lambda full, tag: full + ", " + tag, self._tags, "")

        # Удалим начальные ", "
        tags = tags[2:]
        self._params.set (RootWikiPage.sectionGeneral, WikiPage.paramTags, tags)


    def initAfterCreating (self, tags):
        """
        Инициализация после создания
        """
        self._tags = tags[:]
        self.save()
        self.creationdatetime = datetime.datetime.now()
        self.updateDateTime()
        self.parent.saveChildrenParams()
        self.root.onPageCreate(self)


    def _getTags (self, configParser):
        """
        Выделить теги из строки конфигурационного файла
        """
        try:
            tagsString = configParser.get (RootWikiPage.sectionGeneral, WikiPage.paramTags)
        except ConfigParser.NoOptionError:
            return []

        tags = parseTagsList (tagsString)

        return tags


    @property
    def content(self):
        """
        Прочитать файл-содержимое страницы
        """
        text = ""

        try:
            with open (os.path.join (self.path, RootWikiPage.contentFile)) as fp:
                text = fp.read()
        except IOError:
            pass

        return unicode (text, "utf8", errors="replace")


    @content.setter
    def content (self, text):
        if self.readonly:
            raise ReadonlyException

        if text != self.content or text == u"":
            path = os.path.join (self.path, RootWikiPage.contentFile)

            with open (path, "wb") as fp:
                fp.write (text.encode ("utf8"))

            self.updateDateTime()
            self.root.onPageUpdate(self, change=events.PAGE_UPDATE_CONTENT)


    @property
    def textContent (self):
        """
        Получить контент в текстовом виде.
        Используется для поиска по страницам.
        В большинстве случаев достаточно вернуть просто content
        """
        return self.content


    @property
    def subpath (self):
        result = self.title
        page = self.parent

        while page.parent is not None:
            # Пока не дойдем до корня, у которого нет заголовка, и родитель - None
            result = page.title + "/" + result
            page = page.parent

        return result


    def remove (self):
        """
        Удалить страницу
        """
        if self.readonly:
            raise ReadonlyException

        oldpath = self.path
        tempname = self._getTempName (oldpath)
        oldSelectedPage = self.root.selectedPage

        try:
            os.renames (oldpath, tempname)
            shutil.rmtree (tempname)
        except shutil.Error:
            raise IOError
        except OSError:
            raise IOError

        self.root.onStartTreeUpdate (self.root)
        self._removePageFromTree (self)

        # Если выбранная страница была удалена
        if (oldSelectedPage is not None and
                (oldSelectedPage == self or self.isChild (oldSelectedPage))):
            # Новая выбранная страница взамен старой
            newselpage = oldSelectedPage
            while newselpage.parent is not None and newselpage.isRemoved:
                newselpage = newselpage.parent

            # Если попали в корень дерева
            if newselpage.parent is None:
                newselpage = None

            self.root.selectedPage = newselpage

        self.root.onEndTreeUpdate (self.root)


    def _removePageFromTree (self, page):
        page.parent.removeFromChildren (page)

        for child in page.children:
            page._removePageFromTree (child)

        self.root.onPageRemove (page)


    @property
    def isRemoved (self):
        """
        Проверить, что страница удалена
        """
        return self not in self.parent.children

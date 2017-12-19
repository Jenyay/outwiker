# -*- coding: UTF-8 -*-

import uuid

from outwiker.core.config import StringOption
from outwiker.core.tree import RootWikiPage
from outwiker.core.exceptions import ReadonlyException


class PageUidDepot(object):
    """
    Класс для хранения уникальных идентификаторов страниц и ссылок по ним
    """
    def __init__(self, wikiroot=None):
        """
        wikiroot - корень викидерева или корневая страница.
        Если wikiroot != None, то приосходит поиск всех UID
        """
        self.__configSection = RootWikiPage.sectionGeneral
        self.__configParamName = u"uid"

        # Словарь идентификаторов.
        # Ключ - уникальный идентификатор, значение - указатель на страницу
        self.__uids = {}

        self.__wikiroot = wikiroot

        if wikiroot is not None:
            self.__load(wikiroot)

    def __load(self, root):
        """
        Прочитать UID всех страниц в дереве.
        """
        uid = self.__getUid(root)

        if uid is not None:
            self.__uids[uid] = root

        [self.__load(child) for child in root.children]

    def __getUid(self, page):
        """
        Прочитать и вернуть UID страницы, если он есть.
        Если его нет, возвращается None
        """
        uid = StringOption(page.params,
                           self.__configSection,
                           self.__configParamName,
                           u"").value.lower()

        if len(uid.strip()) == 0:
            uid = None

        return uid

    def __getitem__(self, uid):
        uid = uid.lower()

        page = self.__uids.get(uid, None)

        if page is not None and page.isRemoved:
            del self.__uids[uid]
            page = None

        return page

    def createUid(self, page):
        """
        Сгенерить уникальный идентификатор для страницы и вернуть
        его в качестве значения.
        Если у страницы уже есть идентификатор, возвращаем его
        """
        assert self.__wikiroot is None or page.root == self.__wikiroot

        uid = self.__getUid(page)
        if uid is not None:
            return uid

        # Добавим "__", чтобы было понятно, что в ссылке находится не страница
        uid = self.__generateUid()

        # На случай, если вдруг кто-то поменяет UID страницы, и новый UID с ним
        # совпадет(в этом случае угадавшему UID нужно срочно проверить
        # экстрасенсорные способности :) )
        while uid in self.__uids:
            uid = self.__generateUid()

        self.changeUid(page, uid)

        return uid

    def __generateUid(self):
        return "__" + str(uuid.uuid4())

    def changeUid(self, page, newUid):
        """
        Изменить идентификатор страницы.
        Если новый идентификатор уже существует, бросается исключение KeyError.
        Если идентификатор содержит только пробелы или содержит символ "/",
        бросается исключение ValueError
        """
        if len(newUid.strip()) == 0:
            raise ValueError

        newUid = newUid.lower()

        oldUid = self.__getUid(page)
        if newUid == oldUid:
            return

        if newUid in self.__uids:
            raise KeyError

        # Запрещено использовать "/" в идентификаторе
        if u"/" in newUid:
            raise ValueError

        if page.readonly:
            raise ReadonlyException

        if oldUid in self.__uids:
            del self.__uids[oldUid]

        self.__uids[newUid] = page

        StringOption(page.params,
                     self.__configSection,
                     self.__configParamName,
                     u"").value = newUid

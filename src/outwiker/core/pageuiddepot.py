# -*- coding: utf-8 -*-

from typing import Dict, Optional
import uuid

from outwiker.core.config import StringOption
from outwiker.core.defines import CONFIG_GENERAL_SECTION
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.tree import BasePage, WikiDocument


class PageUidDepot:
    """
    Класс для хранения уникальных идентификаторов страниц и ссылок по ним
    """

    def __init__(self, wikiroot: Optional[WikiDocument] = None):
        """
        wikiroot - корень викидерева или корневая страница.
        Если wikiroot != None, то приосходит поиск всех UID
        """
        self.__configSection = CONFIG_GENERAL_SECTION
        self.__configParamName = "uid"

        # Словарь идентификаторов.
        # Ключ - уникальный идентификатор, значение - указатель на страницу
        self.__uids: Dict[str, BasePage] = {}
        self.load(wikiroot)

    def load(self, wikiroot: Optional[WikiDocument]) -> None:
        self.__uids.clear()

        if wikiroot is not None:
            self.__load(wikiroot)

    def __load(self, root: BasePage):
        """
        Прочитать UID всех страниц в дереве.
        """
        uid = self.__getUid(root)

        if uid is not None:
            self.__uids[uid] = root

        [self.__load(child) for child in root.children]

    def __getUid(self, page: BasePage) -> Optional[str]:
        """
        Прочитать и вернуть UID страницы, если он есть.
        Если его нет, возвращается None
        """
        uid = StringOption(
            page.params, self.__configSection, self.__configParamName, ""
        ).value.lower()

        if len(uid.strip()) == 0:
            uid = None

        return uid

    def __getitem__(self, uid: str) -> Optional[BasePage]:
        uid = uid.lower()

        page = self.__uids.get(uid, None)

        if page is not None and page.getTypeString() != "document" and page.isRemoved:
            del self.__uids[uid]
            page = None

        return page

    def createUid(self, page: BasePage) -> str:
        """
        Сгенерить уникальный идентификатор для страницы и вернуть
        его в качестве значения.
        Если у страницы уже есть идентификатор, возвращаем его
        """
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

    def __generateUid(self) -> str:
        return "__" + str(uuid.uuid4())

    def changeUid(self, page: BasePage, newUid: str) -> None:
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
        if "/" in newUid:
            raise ValueError

        if page.readonly:
            raise ReadonlyException

        if oldUid in self.__uids:
            del self.__uids[oldUid]

        self.__uids[newUid] = page

        StringOption(
            page.params, self.__configSection, self.__configParamName, ""
        ).value = newUid

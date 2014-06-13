# -*- coding: UTF-8 -*-

import uuid

from outwiker.core.config import StringOption
from outwiker.core.tree import RootWikiPage


class PageUidDepot (object):
    """
    Класс для хранения уникальных идентификаторов страниц и ссылок по ним
    """
    def __init__ (self, wikiroot=None):
        """
        wikiroot - корень викидерева или корневая страница. Если wikiroot != None, то приосходит поиск всех UID
        """
        self.__configSection = RootWikiPage.sectionGeneral
        self.__configParamName = u"uid"

        # Словарь идентификаторов.
        # Ключ - уникальный идентификатор, значение - указатель на страницу
        self.__uids = {}

        if wikiroot is not None:
            self.__load (wikiroot)


    def __load (self, root):
        """
        Прочитать UID всех страниц в дереве.
        """
        uid = self.__getUid (root)

        if uid is not None:
            self.__uids[uid] = root

        map (lambda child: self.__load (child), root.children)


    def __getUid (self, page):
        """
        Прочитать и вернуть UID страницы, если он есть. Если его нет, возвращается None
        """
        uid = StringOption (page.params,
                            self.__configSection,
                            self.__configParamName,
                            u"").value

        if len (uid.strip()) == 0:
            uid = None

        return uid


    def __getitem__ (self, uid):
        page = self.__uids.get (uid, None)

        if page is not None and page.isRemoved:
            del self.__uids[uid]
            page = None

        return page


    def createUid (self, page):
        """
        Сгенерить уникальный идентификатор для страницы и вернуть его в качестве значения.
        Если у страницы уже есть идентификатор, возвращаем его
        """
        uid = self.__getUid (page)
        if uid is not None:
            return uid

        uid = unicode (uuid.uuid4())

        # На случай, если вдруг кто-то поменяет UID страницы, и новый UID с ним
        # совпадет (в этом случае угадавшему UID нужно срочно проверить
        # экстрасенсорные способности :) )
        while uid in self.__uids:
            print u" Wow! O_o "
            uid = uuid.uuid4()

        self.__uids[uid] = page

        StringOption (page.params,
                      self.__configSection,
                      self.__configParamName,
                      u"").value = uid

        return uid

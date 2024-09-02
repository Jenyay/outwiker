import configparser
import logging
import os
import os.path
from functools import cmp_to_key

from outwiker.core.exceptions import RootFormatError
from outwiker.core.tree import WikiDocument, WikiPage
from outwiker.core.sortfunctions import sortOrderFunction
from .defines import PAGE_OPT_FILE


logger = logging.getLogger("notesTreeLoader")


class NotesTreeLoader:
    def loadNotesTree(self, path: str, readonly: bool = False) -> WikiDocument:
        """
        Загрузить корневую страницу вики.
        Использовать этот метод вместо конструктора
        """
        logger.debug("Wiki document loading started")
        try:
            root = WikiDocument(path, readonly)
        except configparser.Error:
            raise RootFormatError

        logger.debug("Children notes loading started")
        self._loadChildren(root)
        logger.debug("Children notes loading ended")

        root.onTreeUpdate(root)
        logger.debug("Wiki document loading ended")
        return root

    def _loadChildren(self, parentPage):
        """
        Загрузить дочерние узлы
        """
        try:
            entries = os.listdir(parentPage.path)
        except OSError:
            raise IOError

        children = []

        for name in entries:
            fullpath = os.path.join(parentPage.path, name)
            config_path = os.path.join(fullpath, PAGE_OPT_FILE)

            if (not name.startswith("__") and 
                    os.path.isdir(fullpath) and 
                    os.path.exists(config_path)):
                try:
                    page = self._loadPage(
                        fullpath, parentPage, parentPage.root.readonly
                    )
                except Exception as e:
                    text = "Error reading page {}".format(fullpath)
                    logging.error(text)
                    logging.error("    " + str(e))
                    continue

                children.append(page)

        children.sort(key=cmp_to_key(sortOrderFunction))
        parentPage.children = children
        return children

    def _loadPage(self, path, parent, readonly=False):
        """
        Загрузить страницу.
        Использовать этот метод вместо конструктора,
        когда надо загрузить страницу
        """
        title = os.path.basename(path)
        page = WikiPage(path, title, parent, readonly)
        self._loadChildren(page)
        return page

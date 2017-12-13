# -*- coding: UTF-8 -*-


class TagsList(object):
    """
    Класс для хранения списка всех тегов в вики
    """
    def __init__(self, root):
        self._root = root

        # Словарь тегов. Ключ - тег, значение - список страниц с этим тегом
        self._tags = {}

        self._findTags(root)

    @property
    def tags(self):
        """
        Возвращает список тегов
        """
        return list(self._tags.keys())

    def _findTags(self, page):
        """
        Поиск тегов для страницы page и ее дочерних страниц
        """
        if page.parent is not None:
            for tag in page.tags:
                tag_lower = tag.lower()

                if tag_lower in list(self._tags.keys()):
                    self._tags[tag_lower].append(page)
                else:
                    self._tags[tag_lower] = [page]

        for child in page.children:
            self._findTags(child)

    def __len__(self):
        return len(self._tags)

    def __getitem__(self, tag):
        try:
            pages = self._tags[tag.lower()]
        except KeyError:
            pages = []

        return pages

    def __iter__(self):
        tags = list(self._tags.keys())
        tags.sort()

        return iter(tags)

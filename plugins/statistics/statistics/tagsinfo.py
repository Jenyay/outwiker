# -*- coding: utf-8 -*-

from .i18n import get_


class TagsInfo:
    """Класс для генерации информации о тегах"""

    def __init__(self, frequentTagsList, itemsCount):
        """
        itemsCount - количество выводимых страниц в списках
        """
        self._itemsCount = itemsCount
        self._frequentTagsList = frequentTagsList

        global _
        _ = get_()

    @property
    def content(self):
        tagsCount = self._getTagsCount()
        frequentTags = self._getFrequentTags()
        rarelyTags = self._getRarelyTags()

        return """{tagsCount}
{frequentTags}
{rarelyTags}
<hr/>""".format(
            tagsCount=tagsCount, frequentTags=frequentTags, rarelyTags=rarelyTags
        )

    def _getTagsCount(self):
        """
        Получить оформленное количество тегов
        """
        return "<p>" + _("Tags count: {0}").format(len(self._frequentTagsList)) + "</p>"

    def _getFrequentTags(self):
        title = _("Most frequently used tags:")
        tagsList = self._frequentTagsList[
            0 : min(self._itemsCount, len(self._frequentTagsList))
        ]

        itemsHtml = self._getTagsListHtml(tagsList)
        return """<p>{title}<br>{items}</p>""".format(title=title, items=itemsHtml)

    def _getRarelyTags(self):
        title = _("Most rarely used tags:")

        tagsListAll = self._frequentTagsList[:]
        tagsListAll.reverse()
        tagsList = tagsListAll[0 : min(self._itemsCount, len(self._frequentTagsList))]

        itemsHtml = self._getTagsListHtml(tagsList)
        return """<p>{title}<br>{items}</p>""".format(title=title, items=itemsHtml)

    def _getTagsListHtml(self, tagsList):
        """
        Оформить список тегов в виде HTML
        """
        items = [
            "<li>{title} ({count})</li>".format(title=tagName, count=count)
            for tagName, count in tagsList
        ]

        return "<ul>" + "".join(items) + "</ul>"

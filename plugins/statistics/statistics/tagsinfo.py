#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .i18n import get_


class TagsInfo (object):
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
    def content (self):
        tagsCount = self._getTagsCount()
        frequentTags = self._getFrequentTags()
        rarelyTags = self._getRarelyTags()

        return u"""{tagsCount}
{frequentTags}
{rarelyTags}
<hr/>""".format (tagsCount=tagsCount, frequentTags=frequentTags, rarelyTags=rarelyTags)


    def _getTagsCount (self):
        """
        Получить оформленное количество тегов
        """
        return u"<p>" + _(u"Tags count: {0}").format (len (self._frequentTagsList)) + "</p>"


    def _getFrequentTags (self):
        title = _(u"Most frequently used tags:")
        tagsList = self._frequentTagsList[0: min (self._itemsCount, len (self._frequentTagsList))]

        itemsHtml = self._getTagsListHtml (tagsList)
        return u"""<p>{title}<br>{items}</p>""".format (title=title, items=itemsHtml)


    def _getRarelyTags (self):
        title = _(u"Most rarely used tags:")

        tagsListAll = self._frequentTagsList[:]
        tagsListAll.reverse()
        tagsList = tagsListAll[0: min (self._itemsCount, len (self._frequentTagsList))]

        itemsHtml = self._getTagsListHtml (tagsList)
        return u"""<p>{title}<br>{items}</p>""".format (title=title, items=itemsHtml)


    def _getTagsListHtml (self, tagsList):
        """
        Оформить список тегов в виде HTML
        """
        items = [u"<li>{title} ({count})</li>".format (title=tagName, count=count)
                for tagName, count in tagsList]

        return u"<ul>" + u"".join (items) + u"</ul>"

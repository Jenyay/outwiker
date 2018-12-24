# -*- coding: utf-8 -*-

from .tagscloud import TagsCloud
from .taglabel import EVT_TAG_LEFT_CLICK


class SingleTagSelector (TagsCloud):
    def __init__(self, parent):
        super(SingleTagSelector, self).__init__(parent)

        self.__selectedTag = None
        self.Bind(EVT_TAG_LEFT_CLICK, self.__onTagLeftClick)

    def __onTagLeftClick(self, event):
        self.clearMarks()
        self.__selectedTag = event.text
        self.mark(event.text)

    @property
    def selectedTag(self):
        return self.__selectedTag

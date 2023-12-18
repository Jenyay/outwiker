# -*- coding: utf-8 -*-

from .tagscloud import TagsCloud
from outwiker.gui.controls.taglabel2 import EVT_TAG_LEFT_DOWN


class SingleTagSelector(TagsCloud):
    def __init__(self, parent, enable_active_tags_filter: bool = False):
        super().__init__(
            parent,
            use_buttons=False,
            enable_active_tags_filter=enable_active_tags_filter,
        )

        self.__selectedTag = None
        self.Bind(EVT_TAG_LEFT_DOWN, self.__onTagLeftClick)

    def __onTagLeftClick(self, event):
        self.clearMarks()
        self.__selectedTag = event.text
        self.mark(event.text)

    @property
    def selectedTag(self):
        return self.__selectedTag

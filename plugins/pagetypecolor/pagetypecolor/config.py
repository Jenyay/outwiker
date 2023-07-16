# -*- coding: utf-8 -*-

from outwiker.api.core.config import StringOption


class PageTypeColorConfig:
    """
    Класс для хранения настроек панели с облагом тегов
    """

    SECTION = "PageTypeColor"

    def __init__(self, config):
        self.config = config
        self.wikiColor = StringOption(self.config, self.SECTION, "wiki", "#9DC0FA")
        self.htmlColor = StringOption(self.config, self.SECTION, "html", "#F1F779")
        self.textColor = StringOption(self.config, self.SECTION, "text", "#79F7B8")
        self.searchColor = StringOption(self.config, self.SECTION, "search", "#F280E3")

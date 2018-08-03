# -*- coding: utf-8 -*-

from outwiker.core.config import (BooleanOption,
                                  IntegerOption,
                                  StcStyleOption,
                                  StringOption)
from outwiker.gui.stcstyle import StcStyle


class WikiConfig (object):
    """
    Класс, хранящий указатели на настройки, связанные с викиы
    """
    # Секция конфига для параметров, связанных с викистраницей
    WIKI_PARAM = u"Wiki"

    # Секция, куда записывать параметры стилей оформления редактора
    STYLES_PARAM = u"EditorStyles"

    # Имя параметра "Показывать ли код HTML?"
    SHOW_HTML_CODE_PARAM = u"ShowHtmlCode"

    # Имя параметра для размера превьюшек по умолчанию
    THUMB_SIZE_PARAM = u"ThumbSize"

    # Имя параметра, показывающего, надо ли выводить список
    # прикрепленных файлов вместо пустой страницы
    SHOW_ATTACH_BLANK_PARAM = u"ShowAttachInsteadBlank"

    # Размер превьюшек по умолчанию
    THUMB_SIZE_DEFAULT = 250

    # Имя параметра "Стиль ссылок по умолчанию"
    LINK_STYLE_PARAM = u"DefaultLinkStyle"

    # Стиль ссылок по умолчанию ([[... -> ...]] или [[... | ...]])
    LINK_STYLE_DEFAULT = 0

    # Стили редактора
    STYLE_LINK_PARAM = u"link"
    STYLE_LINK_DEFAULT = StcStyle.parse(u"fore:#0000FF,underline")

    STYLE_HEADING_PARAM = u"heading"
    STYLE_HEADING_DEFAULT = StcStyle.parse(u"bold")

    STYLE_COMMAND_PARAM = u"command"
    STYLE_COMMAND_DEFAULT = StcStyle.parse(u"fore:#6A686B")

    COLORIZE_SYNTAX_PARAM = u'ColorizeSyntax'
    COLORIZE_SYNTAX_DEFAULT = True

    RECENT_STYLE_NAME_PARAM = 'RecentStyleName'
    RECENT_STYLE_NAME_DEFAULT = ''

    def __init__(self, config):
        self.config = config

        # Показывать вкладку с HTML-кодом?
        self.showHtmlCodeOptions = BooleanOption(
            self.config,
            WikiConfig.WIKI_PARAM,
            WikiConfig.SHOW_HTML_CODE_PARAM,
            True)

        # Размер превьюшек по умолчанию
        self.thumbSizeOptions = IntegerOption(self.config,
                                              WikiConfig.WIKI_PARAM,
                                              WikiConfig.THUMB_SIZE_PARAM,
                                              WikiConfig.THUMB_SIZE_DEFAULT)

        # Показывать список прикрепленных файлов вместо пустой страницы?
        self.showAttachInsteadBlankOptions = BooleanOption(
            self.config,
            WikiConfig.WIKI_PARAM,
            WikiConfig.SHOW_ATTACH_BLANK_PARAM,
            True)

        # Стиль ссылок по умолчанию
        self.linkStyleOptions = IntegerOption(self.config,
                                              WikiConfig.WIKI_PARAM,
                                              WikiConfig.LINK_STYLE_PARAM,
                                              WikiConfig.LINK_STYLE_DEFAULT)

        # Стили редактора
        self.link = StcStyleOption(self.config,
                                   WikiConfig.STYLES_PARAM,
                                   WikiConfig.STYLE_LINK_PARAM,
                                   WikiConfig.STYLE_LINK_DEFAULT)

        self.heading = StcStyleOption(self.config,
                                      WikiConfig.STYLES_PARAM,
                                      WikiConfig.STYLE_HEADING_PARAM,
                                      WikiConfig.STYLE_HEADING_DEFAULT)

        self.command = StcStyleOption(self.config,
                                      WikiConfig.STYLES_PARAM,
                                      WikiConfig.STYLE_COMMAND_PARAM,
                                      WikiConfig.STYLE_COMMAND_DEFAULT)

        self.colorizeSyntax = BooleanOption(self.config,
                                            self.WIKI_PARAM,
                                            self.COLORIZE_SYNTAX_PARAM,
                                            self.COLORIZE_SYNTAX_DEFAULT)

        self.recentStyleName = StringOption(self.config,
                                            self.WIKI_PARAM,
                                            self.RECENT_STYLE_NAME_PARAM,
                                            self.RECENT_STYLE_NAME_DEFAULT)

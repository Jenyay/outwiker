# -*- coding: utf-8 -*-

from outwiker.core.config import (BooleanOption,
                                  IntegerOption,
                                  StcStyleOption,
                                  StringOption)
from outwiker.gui.stcstyle import StcStyle


class WikiConfig:
    """
    Класс, хранящий указатели на настройки, связанные с викиы
    """
    # Секция конфига для параметров, связанных с викистраницей
    WIKI_SECTION = "Wiki"

    # Секция, куда записывать параметры стилей оформления редактора
    STYLES_SECTION = "EditorStyles"

    # Имя параметра "Показывать ли код HTML?"
    SHOW_HTML_CODE_PARAM = "ShowHtmlCode"

    # Имя параметра для размера превьюшек по умолчанию
    THUMB_SIZE_PARAM = "ThumbSize"

    # Имя параметра, показывающего, надо ли выводить список
    # прикрепленных файлов вместо пустой страницы
    SHOW_ATTACH_BLANK_PARAM = "ShowAttachInsteadBlank"

    # Размер превьюшек по умолчанию
    THUMB_SIZE_DEFAULT = 250

    # Имя параметра "Стиль ссылок по умолчанию"
    LINK_STYLE_PARAM = "DefaultLinkStyle"

    # Стиль ссылок по умолчанию ([[... -> ...]] или [[... | ...]])
    LINK_STYLE_DEFAULT = 0

    # Стили редактора
    STYLE_LINK_PARAM = "link"
    STYLE_LINK_DEFAULT = StcStyle.parse("fore:#0000FF,underline")

    STYLE_HEADING_PARAM = "heading"
    STYLE_HEADING_DEFAULT = StcStyle.parse("bold")

    STYLE_COMMAND_PARAM = "command"
    STYLE_COMMAND_DEFAULT = StcStyle.parse("fore:#6A686B")

    STYLE_COMMENT_PARAM = "comment"
    STYLE_COMMENT_DEFAULT = StcStyle.parse("fore:#12B535")

    STYLE_ATTACHMENT_PARAM = "attachment"
    STYLE_ATTACHMENT_DEFAULT = StcStyle.parse("fore:#5b81c9,underline")

    STYLE_THUMBNAIL_PARAM = "thumbnail"
    STYLE_THUMBNAIL_DEFAULT = StcStyle.parse("fore:#5b81c9,underline")

    COLORIZE_SYNTAX_PARAM = 'ColorizeSyntax'
    COLORIZE_SYNTAX_DEFAULT = True

    RECENT_STYLE_NAME_PARAM = 'RecentStyleName'
    RECENT_STYLE_NAME_DEFAULT = ''

    def __init__(self, config):
        self.config = config

        # Показывать вкладку с HTML-кодом?
        self.showHtmlCodeOptions = BooleanOption(
            self.config,
            WikiConfig.WIKI_SECTION,
            WikiConfig.SHOW_HTML_CODE_PARAM,
            True)

        # Размер превьюшек по умолчанию
        self.thumbSizeOptions = IntegerOption(self.config,
                                              WikiConfig.WIKI_SECTION,
                                              WikiConfig.THUMB_SIZE_PARAM,
                                              WikiConfig.THUMB_SIZE_DEFAULT)

        # Показывать список прикрепленных файлов вместо пустой страницы?
        self.showAttachInsteadBlankOptions = BooleanOption(
            self.config,
            WikiConfig.WIKI_SECTION,
            WikiConfig.SHOW_ATTACH_BLANK_PARAM,
            True)

        # Стиль ссылок по умолчанию
        self.linkStyleOptions = IntegerOption(self.config,
                                              WikiConfig.WIKI_SECTION,
                                              WikiConfig.LINK_STYLE_PARAM,
                                              WikiConfig.LINK_STYLE_DEFAULT)

        # Стили редактора
        self.link = StcStyleOption(self.config,
                                   WikiConfig.STYLES_SECTION,
                                   WikiConfig.STYLE_LINK_PARAM,
                                   WikiConfig.STYLE_LINK_DEFAULT)

        self.heading = StcStyleOption(self.config,
                                      WikiConfig.STYLES_SECTION,
                                      WikiConfig.STYLE_HEADING_PARAM,
                                      WikiConfig.STYLE_HEADING_DEFAULT)

        self.command = StcStyleOption(self.config,
                                      WikiConfig.STYLES_SECTION,
                                      WikiConfig.STYLE_COMMAND_PARAM,
                                      WikiConfig.STYLE_COMMAND_DEFAULT)

        self.comment = StcStyleOption(self.config,
                                      WikiConfig.STYLES_SECTION,
                                      WikiConfig.STYLE_COMMENT_PARAM,
                                      WikiConfig.STYLE_COMMENT_DEFAULT)

        self.attachment = StcStyleOption(self.config,
                                         WikiConfig.STYLES_SECTION,
                                         WikiConfig.STYLE_ATTACHMENT_PARAM,
                                         WikiConfig.STYLE_ATTACHMENT_DEFAULT)

        self.thumbnail = StcStyleOption(self.config,
                                        WikiConfig.STYLES_SECTION,
                                        WikiConfig.STYLE_THUMBNAIL_PARAM,
                                        WikiConfig.STYLE_THUMBNAIL_DEFAULT)

        self.colorizeSyntax = BooleanOption(self.config,
                                            self.WIKI_SECTION,
                                            self.COLORIZE_SYNTAX_PARAM,
                                            self.COLORIZE_SYNTAX_DEFAULT)

        self.recentStyleName = StringOption(self.config,
                                            self.WIKI_SECTION,
                                            self.RECENT_STYLE_NAME_PARAM,
                                            self.RECENT_STYLE_NAME_DEFAULT)

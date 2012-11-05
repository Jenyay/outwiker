#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.config import BooleanOption, IntegerOption

class WikiConfig (object):
    """
    Класс, хранящий указатели на настройки, связанные с викиы
    """
    # Секция конфига для параметров, связанных с викистраницей
    WIKI_SECTION = u"Wiki"

    # Имя параметра "Показывать ли код HTML?"
    SHOW_HTML_CODE_PARAM = u"ShowHtmlCode"

    # Имя параметра для размера превьюшек по умолчанию
    THUMB_SIZE_PARAM = u"ThumbSize"

    # Имя параметра, показывающего, надо ли выводить список прикрепленных файлов вместо пустой страницы
    SHOW_ATTACH_BLANK_PARAM = u"ShowAttachInsteadBlank"

    # Размер превьюшек по умолчанию
    THUMB_SIZE_DEFAULT = 250

    # Имя параметра "Стиль ссылок по умолчанию"
    LINK_STYLE_PARAM = u"DefaultLinkStyle"

    # Стиль ссылок по умолчанию
    LINK_STYLE_DEFAULT = 0


    def __init__ (self, config):
        self.config = config

        # Показывать вкладку с HTML-кодом?
        self.showHtmlCodeOptions = BooleanOption (self.config, 
                WikiConfig.WIKI_SECTION, 
                WikiConfig.SHOW_HTML_CODE_PARAM,
                True)

        # Размер превьюшек по умолчанию
        self.thumbSizeOptions = IntegerOption (self.config, 
                WikiConfig.WIKI_SECTION, 
                WikiConfig.THUMB_SIZE_PARAM, 
                WikiConfig.THUMB_SIZE_DEFAULT)
        
        # Показывать список прикрепленных файлов вместо пустой страницы?
        self.showAttachInsteadBlankOptions = BooleanOption (self.config, 
                WikiConfig.WIKI_SECTION, 
                WikiConfig.SHOW_ATTACH_BLANK_PARAM, 
                True)

        # Стиль ссылок по умолчанию
        self.linkStyleOptions = IntegerOption (self.config, 
                WikiConfig.WIKI_SECTION, 
                WikiConfig.LINK_STYLE_PARAM, 
                WikiConfig.LINK_STYLE_DEFAULT)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.lexers import ClassNotFound

from .sourceconfig import SourceConfig


class CommandSource (Command):
    """
    Команда source для оформления исходных текстов программ
    Использование:

    (:source params)
    Текст программы
    (:sourceend:)

    Параметры:
    tabwidth - размер табуляции
    lang - язык программирования (пока не используется)
    """
    def __init__ (self, parser, config):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)
        self.__config = SourceConfig (config)

        # Добавлены ли стили в заголовок
        self.__styleAppend = False

    
    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"source"


    def execute (self, params, content):
        """
        Запустить команду на выполнение. 
        Оформление исходных текстов
        """
        params_dict = Command.parseParams (params)

        defaultTabWidth = self.__config.tabWidth.value
        tabWidthParamName = "tabwidth"

        try:
            tabwidth = int (params_dict[tabWidthParamName]) if tabWidthParamName in params_dict else defaultTabWidth
        except ValueError:
            tabwidth = defaultTabWidth

        newcontent = content.replace ("\t", " " * tabwidth)
        colortext = self.__colorize (params_dict, newcontent)

        return colortext


    def __colorize (self, params_dict, content):
        langDefault = "text"
        langParam = u"lang"

        lang = params_dict[langParam] if langParam in params_dict else langDefault

        # Стиль для общего div
        highlightStyle = u'.highlight {border-style: solid; border-color: gray; border-width: 1px; background-color: #eee}'
        sourceStyle = HtmlFormatter().get_style_defs()

        styleTemplate = u"<STYLE>{0}</STYLE>"

        if not self.__styleAppend:
            self.parser.appendToHead (styleTemplate.format (sourceStyle))
            self.parser.appendToHead (styleTemplate.format (highlightStyle))

            self.__styleAppend = True

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = get_lexer_by_name(langDefault, stripall=True)

        formatter = HtmlFormatter(linenos=False)
        result = highlight(content, lexer, formatter)

        result = result.replace ("\n</td>", "</td>")

        return result
        

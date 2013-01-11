#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command
from outwiker.core.attachment import Attachment

from pygments import highlight
from pygments.formatters import HtmlFormatter

from .sourceconfig import SourceConfig
from .lexermaker import LexerMaker
from .i18n import get_
from .params import FILE_PARAM_NAME, ENCODING_PARAM_NAME, ENCODING_DEFAULT, TAB_WIDTH_PARAM_NAME, HIGHLIGHT_STYLE, TAB_WIDTH_DEFAULT
from .misc import getFileName


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
    file - имя прикрепленного файла (с приставкой Attach: или без нее)
    encoding - кодировка для прикрепленного файла (используется вместе с параметром file). Если кодирвока не указана, используется UTF-8
    """
    def __init__ (self, parser, config):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)
        self.__config = SourceConfig (config)

        # Добавлены ли стили в заголовок
        self.__styleAppend = False

        global _
        _ = get_()

    
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

        try:
            sourceText = self.__getContentFromFile (params_dict)
        except KeyError:
            sourceText = content
        except IOError:
            return _(u"<B>Source plugin: File '{0}' not found</B>".format (getFileName (params_dict[FILE_PARAM_NAME])))

        tabwidth = self.__getTabWidth (params_dict)

        newcontent = sourceText.replace ("\t", " " * tabwidth)
        colortext = self.__colorize (params_dict, newcontent)

        return colortext


    def __getTabWidth (self, params_dict):
        """
        Получить размер табуляции в зависимости от параметров
        """
        tabwidth = self.__config.tabWidth.value

        try:
            if TAB_WIDTH_PARAM_NAME in params_dict:
                tabwidth = int (params_dict[TAB_WIDTH_PARAM_NAME])
        except ValueError:
            pass

        if tabwidth <= 0:
            tabwidth = TAB_WIDTH_DEFAULT

        return tabwidth


    def __getContentFromFile (self, params_dict):
        """
        Попытаться прочитать исходник из файла, заданный в параметре FILE_PARAM_NAME
        В начале значения параметра может стоять строка Attach:
        """
        fname = getFileName (params_dict[FILE_PARAM_NAME])

        # Полный путь до прикрепленного файла
        attachPath = Attachment (self.parser.page).getFullPath (fname)

        # Обработка исключений происходит выше (в execute)
        with open (attachPath) as fp:
            sourceTextStr = fp.read()

        encoding = self.__getEncoding (params_dict)

        try:
            sourceText = unicode (sourceTextStr, encoding)
        except UnicodeDecodeError:
            return sourceTextStr
        except LookupError:
            # Введена неизвестная кодировка, попробуем UTF-8
            try:
                sourceText = unicode (sourceTextStr, ENCODING_DEFAULT)
            except UnicodeDecodeError:
                return sourceTextStr

        return sourceText


    def __getEncoding (self, params_dict):
        """
        Выберем кодировку в соответствии с параметрами
        """
        encoding = ENCODING_DEFAULT

        if ENCODING_PARAM_NAME in params_dict:
            encoding = params_dict[ENCODING_PARAM_NAME]

        return encoding


    def __colorize (self, params_dict, content):
        """
        Раскраска исходников. Возвращает получившийся HTML и добавляет нужные стили в заголовок страницы
        """
        lexermaker = LexerMaker ()
        lexer = lexermaker.getLexer (params_dict)

        sourceStyle = HtmlFormatter().get_style_defs()

        styleTemplate = u"<STYLE>{0}</STYLE>"

        if not self.__styleAppend:
            self.parser.appendToHead (styleTemplate.format (sourceStyle))
            self.parser.appendToHead (styleTemplate.format (HIGHLIGHT_STYLE))

            self.__styleAppend = True

        formatter = HtmlFormatter(linenos=False)
        result = highlight(content, lexer, formatter)

        result = result.replace ("\n</td>", "</td>")

        return result
        

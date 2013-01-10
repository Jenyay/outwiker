#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command
from outwiker.pages.wiki.parser.tokenattach import AttachToken
from outwiker.core.attachment import Attachment

from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.lexers import ClassNotFound

from .sourceconfig import SourceConfig
from .i18n import get_


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

        # Имя параметра для указания прикрепленного файла для раскраски
        self.fileParamName = u"file"

        # Имя параметра для указания языка
        self.langParam = u"lang"

        # Язык программирования по умолчанию
        self.langDefault = u"text"

        # Кодировка для прикрепленного файла
        self.encodingParam = "encoding"

        # Используемая кодировка по умолчанию
        self.encodingDefault = "utf8"

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

        defaultTabWidth = self.__config.tabWidth.value

        # Имя параметра для размера табуляции
        tabWidthParamName = u"tabwidth"

        try:
            sourceText = self.__getContentFromFile (params_dict)
        except KeyError:
            sourceText = content
        except IOError:
            return _(u"<B>Source plugin: File '{0}' not found</B>".format (self.__getFileName (params_dict[self.fileParamName])))

        try:
            tabwidth = int (params_dict[tabWidthParamName]) if tabWidthParamName in params_dict else defaultTabWidth
        except ValueError:
            tabwidth = defaultTabWidth

        newcontent = sourceText.replace ("\t", " " * tabwidth)
        colortext = self.__colorize (params_dict, newcontent)

        return colortext


    def __getContentFromFile (self, params_dict):
        """
        Попытаться прочитать исходник из файла, заданный в параметре self.fileParamName
        В начале значения параметра может стоять строка Attach:
        """
        fname = self.__getFileName (params_dict[self.fileParamName])

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
                sourceText = unicode (sourceTextStr, self.encodingDefault)
            except UnicodeDecodeError:
                return sourceTextStr

        return sourceText


    def __getEncoding (self, params_dict):
        """
        Выберем кодировку в соответствии с параметрами
        """
        encoding = self.encodingDefault

        if self.encodingParam in params_dict:
            encoding = params_dict[self.encodingParam]

        return encoding


    def __getFileName (self, fileParam):
        """
        Получить имя прикрепленного файла по параметру file
        fileParam - значение параметра file
        """
        fname = fileParam.strip()

        if fname.startswith (AttachToken.attachString):
            fname = fname[len (AttachToken.attachString): ]

        return fname


    def __getLexer (self, params_dict):
        if self.langParam in params_dict:
            lexer = self.__getLexerByName (params_dict)
        elif self.fileParamName in params_dict:
            lexer = self.__getLexerByFileName (params_dict)
        else:
            lexer = self.__getDefaultLexer()

        return lexer


    def __getLexerByName (self, params_dict):
        """
        Возвращает лексер для нужного языка программирования в зависимости от параметров
        """
        lang = params_dict[self.langParam] if self.langParam in params_dict else self.langDefault
        
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = self.__getDefaultLexer ()

        return lexer


    def __getLexerByFileName (self, params_dict):
        fname = self.__getFileName (params_dict[self.fileParamName])

        try:
            lexer = get_lexer_for_filename (fname, stripall=True)
        except ClassNotFound:
            lexer = self.__getDefaultLexer ()

        return lexer


    def __getDefaultLexer (self):
        """
        Создать лексер по умолчанию
        """
        return get_lexer_by_name(self.langDefault, stripall=True)


    def __colorize (self, params_dict, content):
        """
        Раскраска исходников. Возвращает получившийся HTML и добавляет нужные стили в заголовок страницы
        """
        lexer = self.__getLexer (params_dict)

        # Стиль для общего div
        highlightStyle = u'.highlight {border-style: solid; border-color: gray; border-width: 1px; background-color: #eee; padding-left: 10px;}'
        sourceStyle = HtmlFormatter().get_style_defs()

        styleTemplate = u"<STYLE>{0}</STYLE>"

        if not self.__styleAppend:
            self.parser.appendToHead (styleTemplate.format (sourceStyle))
            self.parser.appendToHead (styleTemplate.format (highlightStyle))

            self.__styleAppend = True

        formatter = HtmlFormatter(linenos=False)
        result = highlight(content, lexer, formatter)

        result = result.replace ("\n</td>", "</td>")

        return result
        

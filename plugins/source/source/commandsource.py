#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command
from outwiker.core.attachment import Attachment

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.styles import STYLE_MAP

from .sourceconfig import SourceConfig
from .lexermaker import LexerMaker
from .i18n import get_
from .params import FILE_PARAM_NAME, ENCODING_PARAM_NAME, ENCODING_DEFAULT, TAB_WIDTH_PARAM_NAME, HIGHLIGHT_STYLE, TAB_WIDTH_DEFAULT, STYLE_PARAM_NAME, STYLE_DEFAULT, PARENT_BACKGROUND_PARAM_NAME
from .misc import getFileName, getDefaultStyle


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

        # Стили, добавленные в заголовок
        self.__appendStyles = []

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
            return _(u"<B>Source plugin: File '{0}' not found</B>").format (getFileName (params_dict[FILE_PARAM_NAME]))

        except UnicodeDecodeError:
            return _(u"<B>Source plugin: Encoding error</B>")

        except LookupError:
            return _(u"<B>Source plugin: Unknown encoding</B>")

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

        return unicode (sourceTextStr, self.__getEncoding (params_dict))


    def __getEncoding (self, params_dict):
        """
        Выберем кодировку в соответствии с параметрами
        """
        encoding = ENCODING_DEFAULT

        if ENCODING_PARAM_NAME in params_dict:
            encoding = params_dict[ENCODING_PARAM_NAME]

        return encoding


    def __getStyle (self, params_dict):
        if (STYLE_PARAM_NAME not in params_dict or
                params_dict[STYLE_PARAM_NAME] not in STYLE_MAP):
            return getDefaultStyle (self.__config)

        return params_dict[STYLE_PARAM_NAME]


    def __getCssClass (self, style, parentBg=False):
        result = u"highlight-" + style
        if parentBg:
            result += "-parentbg"

        return result


    def __colorize (self, params_dict, content):
        """
        Раскраска исходников. Возвращает получившийся HTML и добавляет нужные стили в заголовок страницы
        """
        lexermaker = LexerMaker ()
        lexer = lexermaker.getLexer (params_dict)

        style = self.__getStyle (params_dict)
        cssclass = self.__getCssClass (style, PARENT_BACKGROUND_PARAM_NAME in params_dict)

        formatter = HtmlFormatter(linenos=False, cssclass=cssclass, style=style)
        sourceStyle = formatter.get_style_defs()

        # Нужно для улучшения внешнего вида исходников на страницах с темным фоном
        sourceStyle += u"\n.{name} pre {{padding: 0px; border: none; color: inherit; background-color: inherit }}".format (name=cssclass)
        sourceStyle += u"\n.{name} table {{padding: 0px; border: none;}}".format (name=cssclass)
        sourceStyle += u"\n.source-block pre {{padding: 0px; border: none; color: inherit; background-color: inherit }}"
        sourceStyle += u"\n.{name}table td {{border-width:0}}".format (name=cssclass)
        sourceStyle += u"\n.linenodiv pre {{padding: 0px; border: none; color: inherit; background-color: inherit }}".format (name=style)

        if PARENT_BACKGROUND_PARAM_NAME in params_dict:
            sourceStyle += u"\n.{name} {{color: inherit; background-color: inherit }}".format (name=cssclass)

        styleTemplate = u"<STYLE>{0}</STYLE>"

        if cssclass not in self.__appendStyles:
            self.parser.appendToHead (styleTemplate.format (sourceStyle))
            self.parser.appendToHead (styleTemplate.format ("".join (["div.", cssclass, HIGHLIGHT_STYLE]) ) )

            self.__appendStyles.append (cssclass)

        content = highlight(content, lexer, formatter)

        result = u"".join ([u'<div class="source-block">', content, u'</div>'])
        result = result.replace ("\n</td>", "</td>")

        return result
        

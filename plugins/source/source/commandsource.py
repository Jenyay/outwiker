# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki.parser.command import Command
from outwiker.api.core.attachment import Attachment
from outwiker.core.htmlformatter import HtmlFormatter

from .sourceconfig import SourceConfig
from .lexermaker import LexerMaker
from .i18n import get_
from .params import (
    FILE_PARAM_NAME,
    ENCODING_PARAM_NAME,
    ENCODING_DEFAULT,
    TAB_WIDTH_PARAM_NAME,
    HIGHLIGHT_STYLE,
    TAB_WIDTH_DEFAULT,
    STYLE_PARAM_NAME,
    PARENT_BACKGROUND_PARAM_NAME,
    LINE_NUM_PARAM_NAME,
    CUSTOM_STYLES,
    CSS_SOURCE_PLUGIN,
    CSS_SOURCE_BLOCK,
)
from .misc import getFileName, getDefaultStyle


class CommandSource(Command):
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
     encoding - кодировка для прикрепленного файла
         (используется вместе с параметром file).
         Если кодировка не указана, используется UTF-8
    """

    def __init__(self, parser, config):
        """
        parser - экземпляр парсера
        """
        super().__init__(parser)
        self._config = SourceConfig(config)
        self._html_formatter = HtmlFormatter([CSS_SOURCE_PLUGIN])

        # Стили CSS, добавленные в заголовок
        self.__appendCssClasses = []

        global _
        _ = get_()

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "source"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Оформление исходных текстов
        """
        params_dict = Command.parseParams(params)

        try:
            sourceText = self._getContentFromFile(params_dict)
        except KeyError:
            sourceText = content
        except IOError:
            content = _("Source plugin: File '{}' not found").format(
                getFileName(params_dict[FILE_PARAM_NAME])
            )
            return self._html_formatter.error(content)
        except UnicodeDecodeError:
            content = _("Source plugin: Encoding error")
            return self._html_formatter.error(content)
        except LookupError:
            content = _("Source plugin: Unknown encoding")
            return self._html_formatter.error(content)

        tabwidth = self._getTabWidth(params_dict)

        newcontent = sourceText.replace("\t", " " * tabwidth)
        colortext = self._colorize(params_dict, newcontent)

        return colortext

    def _getTabWidth(self, params_dict):
        """
        Получить размер табуляции в зависимости от параметров
        """
        tabwidth = self._config.tabWidth.value

        try:
            if TAB_WIDTH_PARAM_NAME in params_dict:
                tabwidth = int(params_dict[TAB_WIDTH_PARAM_NAME])
        except ValueError:
            pass

        if tabwidth <= 0:
            tabwidth = TAB_WIDTH_DEFAULT

        return tabwidth

    def _getContentFromFile(self, params_dict):
        """
        Попытаться прочитать исходник из файла,
        заданный в параметре FILE_PARAM_NAME
        В начале значения параметра может стоять строка Attach:
        """
        fname = getFileName(params_dict[FILE_PARAM_NAME])
        fname = fname.replace("\\", "/")
        encoding = self._getEncoding(params_dict)

        # Полный путь до прикрепленного файла
        attachPath = Attachment(self.parser.page).getFullPath(fname)

        # Обработка исключений происходит выше(в execute)
        with open(attachPath, encoding=encoding) as fp:
            sourceTextStr = fp.read()

        return sourceTextStr

    def _getEncoding(self, params_dict):
        """
        Выберем кодировку в соответствии с параметрами
        """
        encoding = ENCODING_DEFAULT

        if ENCODING_PARAM_NAME in params_dict:
            encoding = params_dict[ENCODING_PARAM_NAME]

        return encoding

    def _getStyle(self, params_dict):
        from .pygments.styles import STYLE_MAP

        if (
            STYLE_PARAM_NAME not in params_dict
            or params_dict[STYLE_PARAM_NAME] not in STYLE_MAP
        ):
            return getDefaultStyle(self._config)

        return params_dict[STYLE_PARAM_NAME]

    def _getCssClass(self, style, parentBg=False):
        result = "highlight-" + style
        if parentBg:
            result += "-parentbg"

        return result

    def _colorize(self, params_dict, content):
        """
        Раскраска исходников. Возвращает получившийся HTML и добавляет
        нужные стили в заголовок страницы
        """
        from .pygments import highlight
        from .pygments.formatters import HtmlFormatter

        lexermaker = LexerMaker()
        lexer = lexermaker.getLexer(params_dict)

        linenum = LINE_NUM_PARAM_NAME in params_dict
        parentbg = PARENT_BACKGROUND_PARAM_NAME in params_dict

        style = self._getStyle(params_dict)
        cssclass = self._getCssClass(style, parentbg)

        formatter = HtmlFormatter(linenos=linenum, cssclass=cssclass, style=style)

        if cssclass not in self.__appendCssClasses:
            sourceStyle = formatter.get_style_defs()

            # Нужно для улучшения внешнего вида исходников
            sourceStyle += CUSTOM_STYLES.format(name=cssclass)

            if parentbg:
                sourceStyle += (
                    "\n.{name} {{color: inherit; background-color: inherit }}".format(
                        name=cssclass
                    )
                )

            styleTemplate = "<style>{0}</style>"
            self.parser.appendToHead(styleTemplate.format(sourceStyle))
            self.parser.appendToHead(
                styleTemplate.format("".join(["div.", cssclass, HIGHLIGHT_STYLE]))
            )

            self.__appendCssClasses.append(cssclass)

        content = highlight(content, lexer, formatter)

        result = self._html_formatter.block(content.strip(), [CSS_SOURCE_BLOCK])
        result = result.replace("\n</td>", "</td>")

        return result

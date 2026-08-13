# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki.wikiparser import Command
from outwiker.api.core.attachment import Attachment
from outwiker.api.core.html import HtmlFormatter

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
     Source command for formatting source code.
     Usage:

    (:source params)
     source code
    (:sourceend:)

     Params:
     tabwidth - tab size
     lang - programming language (not used yet)
     file - attached file name (with or without Attach: prefix)
     encoding - encoding for attached file
         (used together with file parameter).
         If encoding is not specified, UTF-8 is used
    """

    def __init__(self, parser, config):
        """
        parser - parser instance
        """
        super().__init__(parser)
        self._config = SourceConfig(config)
        self._html_formatter = HtmlFormatter([CSS_SOURCE_PLUGIN])

        # CSS styles added to the header
        self.__appendCssClasses = []

        global _
        _ = get_()

    @property
    def name(self):
        """
        Returns the command name handled by this class
        """
        return "source"

    def execute(self, params, content):
        """
        Execute the command.
        Format source code.
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
        Get tab width based on parameters
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
        Try to read source code from a file,
        specified in FILE_PARAM_NAME parameter.
        Attach: prefix may be present at the beginning of the parameter value.
        """
        fname = getFileName(params_dict[FILE_PARAM_NAME])
        fname = fname.replace("\\", "/")
        self.parser.addWatchAttachments([fname])
        encoding = self._getEncoding(params_dict)

        # Full path to the attached file
        attachPath = Attachment(self.parser.page).getFullPath(fname)

        # Exception handling is done above (in execute)
        with open(attachPath, encoding=encoding) as fp:
            sourceTextStr = fp.read()

        return sourceTextStr

    def _getEncoding(self, params_dict):
        """
        Select encoding according to parameters
        """
        encoding = ENCODING_DEFAULT

        if ENCODING_PARAM_NAME in params_dict:
            encoding = params_dict[ENCODING_PARAM_NAME]

        return encoding

    def _getStyle(self, params_dict):
        from pygments.styles import STYLE_MAP

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
        Colorize source code. Returns resulting HTML and adds
        required styles to the page header
        """
        from pygments import highlight
        from pygments import formatters

        lexermaker = LexerMaker()
        lexer = lexermaker.getLexer(params_dict)

        linenum = LINE_NUM_PARAM_NAME in params_dict
        parentbg = PARENT_BACKGROUND_PARAM_NAME in params_dict

        style = self._getStyle(params_dict)
        cssclass = self._getCssClass(style, parentbg)

        formatter = formatters.HtmlFormatter(linenos=linenum, cssclass=cssclass, style=style)

        if cssclass not in self.__appendCssClasses:
            sourceStyle = formatter.get_style_defs()

            # Required for better source code appearance
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

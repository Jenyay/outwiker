# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import re

from outwiker.core.defines import (STYLES_BLOCK_FOLDER_NAME,
                                   STYLES_INLINE_FOLDER_NAME,
                                   )
from outwiker.core.standardcolors import standardColorNames
from outwiker.core.system import getSpecialDirList
from outwiker.libs.pyparsing import (Regex, Forward, Literal,
                                     LineStart, LineEnd, NoMatch,
                                     SkipTo)

from .tokennoformat import NoFormatFactory
from ..wikistyleutils import loadCustomStyles


PARAM_NAME_COLOR = 'color'
PARAM_NAME_BACKGROUND_COLOR = 'bgcolor'
PARAM_NAME_STYLE = 'style'


class WikiStyleInlineFactory(object):
    """
    A factory to create inline wiki style tokens.
    """
    @staticmethod
    def make(parser):
        return WikiStyleInline(parser).getToken()


class WikiStyleBlockFactory(object):
    """
    A factory to create block wiki style tokens.
    """
    @staticmethod
    def make(parser):
        return WikiStyleBlock(parser).getToken()


class WikiStyleBase(object, metaclass=ABCMeta):
    def __init__(self, parser):
        self.parser = parser

        styles_folder_name = self._getStylesFolder()
        dir_list = getSpecialDirList(styles_folder_name)
        custom_styles = loadCustomStyles(dir_list)
        self._style_generator = StyleGenerator(custom_styles)

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def _getBeginToken(self):
        pass

    @abstractmethod
    def _getEndToken(self):
        pass

    @abstractmethod
    def _getTag(self):
        pass

    @abstractmethod
    def _getStylesFolder(self):
        pass

    def _getForbiddenToken(self):
        return NoMatch()

    def _prepareContent(self, content):
        return content

    def getToken(self):
        begin = self._getBeginToken()
        end = self._getEndToken().suppress()
        forbidden = self._getForbiddenToken()
        no_format = NoFormatFactory.make(self.parser)

        token = Forward()
        inside = SkipTo(end, failOn=forbidden, ignore=no_format | token).leaveWhitespace()
        token << begin + inside + end

        token = token.setParseAction(self.conversionParseAction)(self.name)

        return token

    def conversionParseAction(self, s, l, t):
        params_list = self._parseParams(t['params'])

        classes, css_list, style = self._style_generator.getStyle(params_list)

        for css in css_list:
            html_style = '<style>{content}</style>\n'.format(content=css)
            if (html_style is not None and
                    html_style not in self.parser.headItems):
                self.parser.appendToHead(html_style)

        classes_str = ' class="' + ' '.join(classes) + '"' if classes else ''
        style_str = ' style="' + style + '"' if style else ''

        content = self._prepareContent(t[1])
        inside = self.parser.parseWikiMarkup(content)
        tag = self._getTag()
        result = '<{tag}{classes}{style}>{inside}</{tag}>'.format(
            tag=tag,
            classes=classes_str,
            style=style_str,
            inside=inside
        )

        return result

    def _parseParams(self, params):
        """
        Parse params string into parts: key - value. Key may contain a dot.
        Sample params:
                param1
                param2 = "bla bla bla"
                param3 = '222'
                param4 = "sample 'bla bla bla' example"
                param5 = 'test "bla-bla-bla" test'
        """
        pattern = r"""((?P<name>#?[\w_-]+)(\s*=\s*(?P<param>(#?[-_\w.]+)|((?P<quote>["']).*?(?P=quote))))?\s*)"""

        result = []

        regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        matches = regex.finditer(params)

        for match in matches:
            name = match.group("name")
            param = match.group("param")
            if param is None:
                param = u""

            result.append((name.lower(), self._removeQuotes(param)))

        return result

    def _removeQuotes(self, text):
        """
        Удалить начальные и конечные кавычки,
        которые остались после разбора параметров
        """
        if (len(text) > 0 and
                (text[0] == text[-1] == "'" or text[0] == text[-1] == '"')):
            return text[1:-1]

        return text


class WikiStyleInline(WikiStyleBase):
    '''
    Token for inline style: %class-name...% ... %%
    '''
    @property
    def name(self):
        return 'style_inline'

    def _getBeginToken(self):
        return Regex(r'%(?P<params>[a-zA-Z_#][\w\s."\'_=:;#(),-]+?)\s*%') + ~LineEnd()

    def _getEndToken(self):
        return Literal('%%')

    def _getTag(self):
        return 'span'

    def _getStylesFolder(self):
        return STYLES_INLINE_FOLDER_NAME

    def _getForbiddenToken(self):
        return Literal('\n\n').leaveWhitespace()


class WikiStyleBlock(WikiStyleBase):
    '''
    Token for block style:
        %class-name...%
        ...
        %%
    '''
    @property
    def name(self):
        return 'style_block'

    def _getBeginToken(self):
        return (LineStart()
                + Regex(r'%(?P<params>[a-zA-Z_#][\w\s."\'_=:;#(),-]+?)\s*%[ \t]*')
                + LineEnd().suppress()
                )

    def _getEndToken(self):
        return LineStart() + Regex(r'%%[ \t]*') + LineEnd()

    def _getTag(self):
        return 'div'

    def _prepareContent(self, content):
        if content.endswith('\n'):
            content = content[:-1]
        return content

    def _getStylesFolder(self):
        return STYLES_BLOCK_FOLDER_NAME


class StyleGenerator(object):
    def __init__(self, custom_styles):
        '''
        custom_styles - dictionary. A key is style name,
            a value is CSS description.
        If inline is True then CSS will be created for the <span> tag else for
            the <div> tag.
        '''
        self._custom_styles = custom_styles

        self._class_name_tpl = 'style-{index}'
        self._class_name_index = 1

        # Key - string of params, value - style name.
        self._added_special_styles = {}

    def getStyle(self, params_list):
        '''
        params_list - list of tuples (param name, value).
        Return tuple: (style name; CSS string).
        '''
        css_list = []
        classes = []
        style = ''

        color = None
        bgcolor = None
        other_styles = None

        for param, value in params_list:
            if not value:
                class_name = param

                if class_name in self._custom_styles:
                    classes.append(class_name)
                    css = self._custom_styles[class_name]
                    css_list.append(css)
                elif class_name in standardColorNames or param.startswith('#'):
                    color = param
                elif ((class_name.startswith('bg-') or
                        class_name.startswith('bg_')) and
                        class_name[3:] in standardColorNames):
                    bgcolor = class_name[3:]
                else:
                    classes.append(class_name)
            elif param == PARAM_NAME_COLOR:
                color = value
            elif param == PARAM_NAME_BACKGROUND_COLOR:
                bgcolor = value
            elif param == PARAM_NAME_STYLE:
                other_styles = value

        style = self._createCSS(color, bgcolor, other_styles)
        return (classes, css_list, style)

    def _createCSS(self, color=None, bgcolor=None, other_styles=None):
        result = ''

        if color:
            result += ' color: {color};'.format(color=color)

        if bgcolor:
            result += ' background-color: {bgcolor};'.format(bgcolor=bgcolor)

        if other_styles:
            other_styles = other_styles.strip()
            if not other_styles.endswith(';'):
                other_styles += ';'

            result += ' ' + other_styles

        return result.strip()

    def _calcHash(self, params_list):
        result = ''
        for param, value in params_list:
            result += param + '=' + value

        return result

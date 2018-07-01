# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import os.path
import re

from outwiker.core.defines import WIKISTYLES_FILE_NAME
from outwiker.core.textstyles import TextStylesStorage
from outwiker.core.system import getStylesDirList
from outwiker.libs.pyparsing import (Regex, Forward, ZeroOrMore, Literal,
                                     LineStart, LineEnd,
                                     SkipTo, originalTextFor)
from outwiker.utilites.textfile import readTextFile

from .tokennoformat import NoFormatFactory


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
        custom_styles = self._loadCustomStyles()
        self._style_generator = StyleGenerator(custom_styles, self._getTag())

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

    def _loadCustomStyles(self):
        storage = TextStylesStorage()

        for style_dir in getStylesDirList():
            fname = os.path.join(style_dir, WIKISTYLES_FILE_NAME)
            try:
                css = readTextFile(fname)
                storage.addStylesFromString(css)
            except IOError:
                pass

        tag = self._getTag()
        result = {name[len(tag) + 1:]: style
                  for name, style
                  in storage.filterByTag(tag).items()}
        return result

    def getToken(self):
        begin = self._getBeginToken()
        end = self._getEndToken().suppress()

        token = Forward()
        no_format = NoFormatFactory.make(self.parser)

        before_end = SkipTo(no_format, failOn=end, ignore=no_format)
        nested_tokens = ZeroOrMore(SkipTo(token, failOn=end, ignore=no_format) + token)

        inside = originalTextFor(nested_tokens + before_end + SkipTo(end)).leaveWhitespace()
        token << begin + inside + end

        token = token.setParseAction(self.conversionParseAction)(self.name)

        return token

    def conversionParseAction(self, s, l, t):
        params_list = self._parseParams(t['params'])

        classes, css_list = self._style_generator.getStyle(params_list)

        for css in css_list:
            html_style = '<style>{content}</style>\n'.format(content=css)
            if (html_style is not None and
                    html_style not in self.parser.headItems):
                self.parser.appendToHead(html_style)

        classes_str = ' class="' + ' '.join(classes) + '"' if classes else ''

        inside = self.parser.parseWikiMarkup(t[1])
        tag = self._getTag()
        result = '<{tag}{classes}>{inside}</{tag}>'.format(
            tag=tag,
            classes=classes_str,
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

            result.append((name.lower(), self._removeQuotes(param.lower())))

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
    Token for inline style: %%class-name...%% ... %%
    '''
    @property
    def name(self):
        return 'style_inline'

    def _getBeginToken(self):
        return Regex(r'%\s*(?P<params>[\w\s."\'_=:;#(),-]+?)\s*%')

    def _getEndToken(self):
        return Literal('%%')

    def _getTag(self):
        return 'span'


class WikiStyleBlock(WikiStyleBase):
    '''
    Token for block style:
        >>class-name...<<
        ...
        >><<
    '''
    @property
    def name(self):
        return 'style_block'

    def _getBeginToken(self):
        return (LineStart()
                + Regex(r'>>\s*(?P<params>[\w\s."\'_=:;#(),-]+?)\s*<<[ \t]*')
                + LineEnd().suppress()
                )

    def _getEndToken(self):
        return LineStart() + Regex(r'>><<[ \t]*') + LineEnd()

    def _getTag(self):
        return 'div'


class StyleGenerator(object):
    def __init__(self, custom_styles, tagname):
        '''
        custom_styles - dictionary. A key is style name,
            a value is CSS description.
        If inline is True then CSS will be created for the <span> tag else for
            the <div> tag.
        '''
        self._standardColors = set([
            "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure",
            "beige", "bisque", "black", "blanchedalmond", "blue", "blueviolet",
            "brown", "burlywood", "cadetblue", "chartreuse", "chocolate",
            "coral", "cornflowerblue", "cornsilk", "crimson", "cyan",
            "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen",
            "darkgrey", "darkkhaki", "darkmagenta", "darkolivegreen",
            "darkorange", "darkorchid", "darkred", "darksalmon",
            "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey",
            "darkturquoise", "darkviolet", "deeppink", "deepskyblue",
            "dimgray", "dimgrey", "dodgerblue", "firebrick", "floralwhite",
            "forestgreen", "fuchsia", "gainsboro", "ghostwhite", "gold",
            "goldenrod", "gray", "green", "greenyellow", "grey", "honeydew",
            "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender",
            "lavenderblush", "lawngreen", "lemonchiffon", "lightblue",
            "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray",
            "lightgreen", "lightgrey", "lightpink", "lightsalmon",
            "lightseagreen", "lightskyblue", "lightslategray",
            "lightslategrey", "lightsteelblue", "lightyellow", "lime",
            "limegreen", "linen", "magenta", "maroon", "mediumaquamarine",
            "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen",
            "mediumslateblue", "mediumspringgreen", "mediumturquoise",
            "mediumvioletred", "midnightblue", "mintcream", "mistyrose",
            "moccasin", "navajowhite", "navy", "oldlace", "olive",
            "olivedrab", "orange", "orangered", "orchid", "palegoldenrod",
            "palegreen", "paleturquoise", "palevioletred", "papayawhip",
            "peachpuff", "peru", "pink", "plum", "powderblue", "purple", "red",
            "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown",
            "seagreen", "seashell", "sienna", "silver", "skyblue", "slateblue",
            "slategray", "slategrey", "snow", "springgreen", "steelblue",
            "tan", "teal", "thistle", "tomato", "turquoise", "violet", "wheat",
            "white", "whitesmoke", "yellow", "yellowgreen",
        ])
        self._custom_styles = custom_styles
        self._tagname = tagname

        self._class_name_tpl = 'style-{index}'
        self._class_name_index = 1

        # Key - string of params, value - style name.
        self._added_special_styles = {}

        # Set of standard and custom styles name
        self._added_styles = set()

    def getStyle(self, params_list):
        '''
        params_list - list of tuples (param name, value).
        Return tuple: (style name; CSS string).
        '''
        css_list = []
        classes = []

        color = None
        bgcolor = None
        other_styles = None

        for param, value in params_list:
            param = param.lower()
            if not value:
                class_name = param

                if class_name in self._custom_styles:
                    classes.append(class_name)
                    css = self._custom_styles[class_name]
                    if class_name not in self._added_styles:
                        css_list.append(css)
                        self._added_styles.add(class_name)

                elif class_name in self._standardColors or param.startswith('#'):
                    color = param
                elif ((class_name.startswith('bg-') or
                        class_name.startswith('bg_')) and
                        class_name[3:] in self._standardColors):
                    bgcolor = class_name[3:]
                else:
                    classes.append(class_name)
            elif param == PARAM_NAME_COLOR:
                color = value
            elif param == PARAM_NAME_BACKGROUND_COLOR:
                bgcolor = value
            elif param == PARAM_NAME_STYLE:
                other_styles = value

        # Custom styles or standard color only
        if not color and not bgcolor and not other_styles:
            return (classes, css_list)

        # For standard color only
        if (color and color in self._standardColors and
                not bgcolor and not other_styles):
            class_name = color
            classes.append(class_name)
            if class_name not in self._added_styles:
                css = self._createCSS(class_name, color)
                css_list.append(css)
            return (classes, css_list)

        # For standard background color only
        if (bgcolor and bgcolor in self._standardColors and
                not color and not other_styles):
            class_name = 'bg-' + bgcolor
            classes.append(class_name)
            if class_name not in self._added_styles:
                css = self._createCSS(class_name, bgcolor=bgcolor)
                css_list.append(css)
            return (classes, css_list)

        hash = self._calcHash(params_list)
        if hash not in self._added_special_styles:
            class_name = self._class_name_tpl.format(
                index=self._class_name_index)
            self._class_name_index += 1

            classes.append(class_name)
            css = self._createCSS(class_name, color, bgcolor, other_styles)
            css_list.append(css)
            self._added_special_styles[hash] = class_name
        else:
            class_name = self._added_special_styles[hash]
            classes.append(class_name)

        return (classes, css_list)

    def _createCSS(self, class_name,
                   color=None, bgcolor=None, other_styles=None):
        result = '{tag}.{name} {{'.format(tag=self._tagname, name=class_name)

        if color:
            result += ' color: {color};'.format(color=color)

        if bgcolor:
            result += ' background-color: {bgcolor};'.format(bgcolor=bgcolor)

        if other_styles:
            other_styles = other_styles.strip()
            if not other_styles.endswith(';'):
                other_styles += ';'

            result += ' ' + other_styles

        result += ' }'
        return result

    def _calcHash(self, params_list):
        result = ''
        for param, value in params_list:
            result += param + '=' + value

        return result

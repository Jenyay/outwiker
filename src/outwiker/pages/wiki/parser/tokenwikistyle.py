# -*- coding: utf-8 -*-

import re

from outwiker.libs.pyparsing import (Regex, Forward, ZeroOrMore, Literal,
                                     SkipTo, originalTextFor)

from .tokennoformat import NoFormatFactory


COLOR_PARAM_NAME = 'color'
# BACKGROUND_COLOR_PARAM_NAME = 'bgcolor'


class WikiStyleInlineFactory(object):
    """
    The fabric to create inline wiki style tokens.
    """
    @staticmethod
    def make(parser):
        return WikiStyleInline(parser).getToken()


class WikiStyleInline(object):
    start_html = ''
    end_html = '</span>'
    name = 'wikistyle_inline'

    def __init__(self, parser):
        self.parser = parser
        custom_styles = {}
        self._style_generator = StyleGenerator(custom_styles, True)

    def getToken(self):
        start = Regex(r'%\s*(?P<params>[\w\s."\'_=:;#()-]+?)\s*%')
        end = Literal('%%')

        token = Forward()
        no_format = NoFormatFactory.make(self.parser)

        before_end = SkipTo(no_format, failOn=end, ignore=no_format)
        nested_tokens = ZeroOrMore(SkipTo(token, failOn=end, ignore=no_format) + token)

        inside = originalTextFor(nested_tokens + before_end + SkipTo(end)).leaveWhitespace()
        token << start + inside + end

        token = token.setParseAction(self.conversionParseAction)(self.name)

        return token

    def conversionParseAction(self, s, l, t):
        params_list = self._parseParams(t['params'])
        inside = self.parser.parseWikiMarkup(t[1])

        classes, css_list = self._style_generator.get_style(params_list)

        for css in css_list:
            html_style = '<style>{content}</style>\n'.format(content=css)
            if (html_style is not None and
                    html_style not in self.parser.headItems):
                self.parser.appendToHead(html_style)

        classes_str = ' class="' + ' '.join(classes) + '"' if classes else ''

        result = '<span{classes}>{inside}</span>'.format(
            classes=classes_str,
            inside=inside
        )

        return result

    def _parseParams(self, params):
        """
        Parse params string into parts: key - value. Key may contain a dot.
        Sample params:
            param1 Параметр2.subparam = 111 Параметр3 = " bla bla bla" param4.sub.param2 = "111" param5 =' 222 ' param7 = " sample 'bla bla bla' example" param8 = ' test "bla-bla-bla" test '
        """
        pattern = r"""((?P<name>#?[\w.-]+)(\s*=\s*(?P<param>([-_\w.]+)|((?P<quote>["']).*?(?P=quote)) ) )?\s*)"""

        result = []

        regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        matches = regex.finditer(params)

        for match in matches:
            name = match.group("name")
            param = match.group("param")
            if param is None:
                param = u""

            result.append((name, self._removeQuotes(param)))

        return result

    def _removeQuotes(self, text):
        """
        Удалить начальные и конечные кавычки, которые остались после разбора параметров
        """
        if (len(text) > 0 and
                (text[0] == text[-1] == "'" or text[0] == text[-1] == '"')):
            return text[1:-1]

        return text


class StyleNotFound(Exception):
    def __init__(self, style_name):
        self.message = 'Style "{}" is not found'.format(style_name)


class StyleGenerator(object):
    def __init__(self, custom_styles, inline):
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
        self._inline = inline

        # Key - string with params, value - tuple (style name; CSS string).
        # self._cache = {}

    def get_style(self, params_list):
        '''
        params_list - list of tuples (param name, value).
        Return tuple: (style name; CSS string).
        '''
        bgcolor = None
        other_styles = None

        color = self._get_color(params_list)
        classes = self._get_classes(color, bgcolor, other_styles, params_list)

        css_list = self._create_css_list(classes, color, bgcolor, other_styles)
        return (classes, css_list)

    def _get_color(self, params_list):
        for param, value in params_list:
            param = param.lower()
            if not value:
                if param in self._standardColors:
                    return param

    def _get_classes(self, color, bgcolor, other_styles, params_list):
        classes = []
        for param, value in params_list:
            param = param.lower()
            if not value:
                classes.append(param)

        if color and color not in classes and not bgcolor and not other_styles:
            if color in self._standardColors:
                classes.append(color)

        return classes

    def _create_css_list(self, classes, color, bgcolor, other_styles):
        css_list = []
        for style_name in classes:
            if style_name in self._custom_styles:
                css_list.append(self._custom_styles[style_name])

        if color is None and bgcolor is None and other_styles is None:
            return css_list

        tag = self._get_tag()
        result = '{tag}.{name} {{'.format(tag=tag, name=style_name)

        if color is not None:
            result += ' color: {color};'.format(color=color)

        result += ' }'
        css_list.append(result)

        return css_list

    def _get_tag(self):
        return 'span' if self._inline else 'div'

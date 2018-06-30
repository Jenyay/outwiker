# -*- coding: utf-8 -*-

import re

from outwiker.libs.pyparsing import (Regex, Forward, ZeroOrMore, Literal,
                                     SkipTo, originalTextFor)

from .tokennoformat import NoFormatFactory


PARAM_NAME_COLOR = 'color'
# PARAM_NAME_BACKGROUND_COLOR = 'bgcolor'


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
        start = Regex(r'%\s*(?P<params>[\w\s."\'_=:;#(),-]+?)\s*%')
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

        classes, css_list = self._style_generator.get_style(params_list)

        for css in css_list:
            html_style = '<style>{content}</style>\n'.format(content=css)
            if (html_style is not None and
                    html_style not in self.parser.headItems):
                self.parser.appendToHead(html_style)

        classes_str = ' class="' + ' '.join(classes) + '"' if classes else ''

        inside = self.parser.parseWikiMarkup(t[1])
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
        pattern = r"""((?P<name>#?[\w.-]+)(\s*=\s*(?P<param>(#?[-_\w.]+)|((?P<quote>["']).*?(?P=quote))))?\s*)"""

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

        self._class_name_tpl = 'style-{index}'
        self._class_name_index = 1

        # Key - string of params, value - style name.
        self._added_special_styles = {}

        # Set of standard and custom styles name
        self._added_styles = set()

    def get_style(self, params_list):
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

                elif class_name in self._standardColors:
                    classes.append(class_name)
                    css = self._create_css(class_name, color=class_name)
                    if class_name not in self._added_styles:
                        css_list.append(css)
                        self._added_styles.add(class_name)
                elif param.startswith('#'):
                    color = param
                else:
                    classes.append(class_name)
            elif param == PARAM_NAME_COLOR:
                color = value

        if not color and not bgcolor and not other_styles:
            return (classes, css_list)

        if (color and color in self._standardColors and
                not bgcolor and not other_styles):
            class_name = color
            classes.append(class_name)
            if class_name not in self._added_styles:
                css = self._create_css(class_name, color=color)
                css_list.append(css)
            return (classes, css_list)

        hash = self._calc_hash(params_list)
        if hash not in self._added_special_styles:
            class_name = self._class_name_tpl.format(
                index=self._class_name_index)
            self._class_name_index += 1

            classes.append(class_name)
            css = self._create_css(class_name, color=color)
            css_list.append(css)
            self._added_special_styles[hash] = class_name
        else:
            class_name = self._added_special_styles[hash]
            classes.append(class_name)

        return (classes, css_list)

    def _create_css(self, class_name,
                    color=None, bgcolor=None, other_styles=None):
        tag = self._get_tag()
        result = '{tag}.{name} {{'.format(tag=tag, name=class_name)

        if color is not None:
            result += ' color: {color};'.format(color=color)

        result += ' }'
        return result

    def _get_tag(self):
        return 'span' if self._inline else 'div'

    def _calc_hash(self, params_list):
        result = ''
        for param, value in params_list:
            result += 'param' + '=' + value

        return result

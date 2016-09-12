# -*- coding: UTF-8 -*-


class TextBlockToken (object):
    """
    Класс, содержащий метод для оборачивания текста в теги текстового уровня
    """
    def __init__(self, parser):
        self.parser = parser

    def convertToHTML(self, opening, closing):
        """
        opening - открывающийся тег(и)
        closing - закрывающийся тег(и)
        """
        def conversionParseAction(s, l, t):
            return u"".join([
                opening,
                self.parser.parseTextLevelMarkup(u''.join(t)),
                closing,
            ])
        return conversionParseAction

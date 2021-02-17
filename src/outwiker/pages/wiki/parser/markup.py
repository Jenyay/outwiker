# coding: utf-8

from pyparsing import NoMatch


class Markup:
    def __init__(self, tokens_list):
        self._markup = NoMatch()
        for token in tokens_list:
            self._markup |= token

    def transformString(self, text):
        return self._markup.transformString(text)

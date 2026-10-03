# coding: utf-8

from pyparsing import NoMatch


class Markup:
    def __init__(self, tokens_list):
        self._markup = NoMatch()
        for token in tokens_list:
            self._markup |= token

    def transform_string(self, text):
        return self._markup.transform_string(text)

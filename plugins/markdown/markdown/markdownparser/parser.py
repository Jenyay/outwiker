# -*- coding: UTF-8 -*-

from markdown_plugin_libs.markdown import markdown


class Parser (object):
    def __init__(self):
        pass

    def convert(self, text):
        result = markdown(text, output_format='html5')
        return result

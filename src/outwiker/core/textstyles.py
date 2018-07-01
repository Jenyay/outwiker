# -*- coding: utf-8 -*-

import re


class TextStylesStorage(object):
    def __init__(self):
        # Key - style name like div.warning, span.error;
        # value - full style description.
        self._styles = {}

        self.css_regex = re.compile(r'(?P<name>[\w_.-]+)\s*?\{.*?\}',
                                    re.M | re.S)

    def addStylesFromString(self, css):
        '''
        Add new styles. Existing styles of the same name will be replaced.
        '''
        for match in self.css_regex.finditer(css):
            self._styles[match['name'].strip()] = match[0].strip()

    def filterByTag(self, tag):
        '''
        Return dictionary with styles for special tag only
        '''
        tag = tag.lower()
        result = {}
        for name, style in self._styles.items():
            if name.lower().startswith(tag + '.'):
                result[name] = style

        return result

    def getStyles(self):
        '''
        Return all styles
        '''
        return self._styles

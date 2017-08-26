# -*- coding: utf-8 -*-

from .libs.jinja2 import Environment


class ContentGenerator(object):
    def __init__(self, templateStr):
        self._templateStr = templateStr

    def render(self, data):
        '''
        data - dictionary for template substitution.
        '''
        env = Environment()
        templateObj = env.from_string(self._templateStr)

        return templateObj.render(**data)

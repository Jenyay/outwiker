# -*- coding: utf-8 -*-


class ContentGenerator(object):
    def __init__(self, templateStr):
        self._templateStr = templateStr

    def render(self, data):
        '''
        data - dictionary for template substitution.
        '''
        from .libs.jinja2 import Environment

        env = Environment()
        templateObj = env.from_string(self._templateStr)

        return templateObj.render(**data)

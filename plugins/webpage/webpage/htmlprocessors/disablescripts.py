# -*- coding: UTF-8 -*-


def disableScripts (params):
    if params.page.disableScripts:
        map (lambda tag: tag.extract(), params.soup('script'))

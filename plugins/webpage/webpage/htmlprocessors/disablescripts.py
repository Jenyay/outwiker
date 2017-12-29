# -*- coding: utf-8 -*-


def disableScripts(params):
    assert params.page is not None
    if params.page.disableScripts:
        [*map(lambda tag: tag.extract(), params.soup('script'))]

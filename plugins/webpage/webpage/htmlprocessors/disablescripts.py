# -*- coding: utf-8 -*-
from ..webnotepage import WebPageFactory


def disableScripts(params):
    assert params.page is not None
    page_adapter = WebPageFactory().createPageAdapter(params.page)
    if page_adapter.disableScripts:
        [*map(lambda tag: tag.extract(), params.soup("script"))]

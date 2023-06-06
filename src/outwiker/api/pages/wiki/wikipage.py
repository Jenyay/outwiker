from typing import List

import outwiker.core.factory as _factory
import outwiker.pages.wiki.wikipage as _wikipage


def createWikiPage(parent, alias: str, tags: List[str], order_calculator = _factory.orderCalculatorBottom):
    return _wikipage.WikiPageFactory().create(parent, alias, tags, order_calculator)

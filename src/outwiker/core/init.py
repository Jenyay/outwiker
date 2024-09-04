from outwiker.core.factoryselector import addPageFactory, FactorySelector
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory


def init_page_factories():
    FactorySelector.reset()
    addPageFactory(WikiPageFactory())
    addPageFactory(HtmlPageFactory())
    addPageFactory(TextPageFactory())
    addPageFactory(SearchPageFactory())

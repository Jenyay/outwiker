# -*- coding: utf-8 -*-

import os
import shutil
from collections.abc import Iterator
from tempfile import mkdtemp

import pytest

from outwiker.api.core.tree import createNotesTree
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.core.tree import WikiDocument
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.utils import removeDir


WIKI_PAGE_TITLE = "Викистраница 1"
HTML_PAGE_TITLE = "Html-страница 2"

STYLE_FNAME = "__style.html"
STYLE_DIRNAME = "__style"

EXAMPLE_STYLE_DIR = "testdata/styles/example_jblog/example_jblog"
EXAMPLE_STYLE_DIR2 = "testdata/styles/example_jnet/example_jnet"
INVALID_STYLE_DIR = "../styles/invalid"
TEST_STYLE_PATH = os.path.join(EXAMPLE_STYLE_DIR, STYLE_FNAME)
DEFAULT_STYLE_PATH = "src/outwiker/data/styles/__default/__style.html"


@pytest.fixture
def test_wikiroot(application: Application) -> Iterator[WikiDocument]:
    """
    Create a wiki with one wiki page and one HTML page and open it in the
    application for the duration of the test.
    """
    path = mkdtemp(prefix="Абырвалг абыр")
    wikiroot = createNotesTree(path)
    WikiPageFactory().create(wikiroot, WIKI_PAGE_TITLE, [])
    HtmlPageFactory().create(wikiroot, HTML_PAGE_TITLE, [])

    application.wikiroot = wikiroot

    yield wikiroot

    application.wikiroot = None
    removeDir(path)


@pytest.fixture
def page_update_events(application: Application) -> Iterator[list]:
    """
    Collect the senders of the onPageUpdate events fired during the test.
    """
    senders = []

    def on_page_update(sender, **kwargs):
        senders.append(sender)

    application.onPageUpdate += on_page_update

    yield senders

    application.onPageUpdate -= on_page_update


def test_default():
    """
    Check that the path to the default template is returned.
    """
    style = Style()
    default_style = style.getDefaultStyle()

    assert os.path.abspath(default_style) == os.path.abspath(DEFAULT_STYLE_PATH)


def test_style_page_default(test_wikiroot: WikiDocument):
    """
    Check that pages without a style file use the default style.
    """
    style = Style()
    default_style = style.getDefaultStyle()

    style_page1 = style.getPageStyle(test_wikiroot[WIKI_PAGE_TITLE])
    style_page2 = style.getPageStyle(test_wikiroot[HTML_PAGE_TITLE])

    assert style_page1 == default_style
    assert style_page2 == default_style


def test_style_page_1(test_wikiroot: WikiDocument):
    page = test_wikiroot[WIKI_PAGE_TITLE]
    shutil.copy(TEST_STYLE_PATH, page.path)

    valid_style = os.path.abspath(os.path.join(page.path, STYLE_FNAME))
    page_style = os.path.abspath(Style().getPageStyle(page))

    assert page_style == valid_style


def test_style_page_2(test_wikiroot: WikiDocument):
    page = test_wikiroot[HTML_PAGE_TITLE]
    shutil.copy(TEST_STYLE_PATH, page.path)

    valid_style = os.path.abspath(os.path.join(page.path, STYLE_FNAME))
    page_style = os.path.abspath(Style().getPageStyle(page))

    assert page_style == valid_style


def test_fake_style(test_wikiroot: WikiDocument):
    """
    A directory named like a style file must not be treated as a style.
    """
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]
    os.mkdir(os.path.join(page.path, STYLE_FNAME))

    valid_style = os.path.abspath(style.getDefaultStyle())
    page_style = os.path.abspath(style.getPageStyle(page))

    assert page_style == valid_style


def test_set_style_as_dir(test_wikiroot: WikiDocument):
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]

    page_style_fname = os.path.join(page.path, STYLE_FNAME)
    page_style_dir = os.path.join(page.path, STYLE_DIRNAME)

    assert not os.path.exists(page_style_dir)
    assert not os.path.exists(page_style_fname)

    style.setPageStyle(page, EXAMPLE_STYLE_DIR)

    assert os.path.exists(page_style_dir)
    assert os.path.exists(page_style_fname)

    style.setPageStyleDefault(page)

    assert not os.path.exists(page_style_dir)
    assert not os.path.exists(page_style_fname)


def test_set_style_as_file(test_wikiroot: WikiDocument):
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]

    page_style_fname = os.path.join(page.path, STYLE_FNAME)
    page_style_dir = os.path.join(page.path, STYLE_DIRNAME)

    assert not os.path.exists(page_style_dir)
    assert not os.path.exists(page_style_fname)

    style.setPageStyle(page, os.path.join(EXAMPLE_STYLE_DIR, STYLE_FNAME))

    assert os.path.exists(page_style_dir)
    assert os.path.exists(page_style_fname)

    style.setPageStyleDefault(page)

    assert not os.path.exists(page_style_dir)
    assert not os.path.exists(page_style_fname)


def test_set_style_2(test_wikiroot: WikiDocument):
    """
    Setting the default style explicitly must remove the page style.
    """
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]

    page_style_fname = os.path.join(page.path, STYLE_FNAME)
    page_style_dir = os.path.join(page.path, STYLE_DIRNAME)

    assert not os.path.exists(page_style_dir)
    assert not os.path.exists(page_style_fname)

    style.setPageStyle(page, EXAMPLE_STYLE_DIR)

    assert os.path.exists(page_style_dir)
    assert os.path.exists(page_style_fname)

    style.setPageStyle(page, style.getDefaultStyle())

    assert not os.path.exists(page_style_dir)
    assert not os.path.exists(page_style_fname)


def test_event(test_wikiroot: WikiDocument, page_update_events: list):
    """
    Changing the page style must fire the page update event.
    """
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]

    assert len(page_update_events) == 0

    style.setPageStyle(page, EXAMPLE_STYLE_DIR)
    assert len(page_update_events) == 1

    style.setPageStyleDefault(page)
    assert len(page_update_events) == 2

    style.setPageStyle(page, EXAMPLE_STYLE_DIR2)
    assert len(page_update_events) == 3


def test_invalid_page(test_wikiroot: WikiDocument):
    """
    Passing None or a wiki root instead of a page must not raise an exception.
    """
    style = Style()
    style.setPageStyle(None, EXAMPLE_STYLE_DIR)
    style.setPageStyleDefault(None)

    style.setPageStyle(test_wikiroot, EXAMPLE_STYLE_DIR)
    style.setPageStyleDefault(test_wikiroot)


def test_invalid_path(test_wikiroot: WikiDocument):
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]

    with pytest.raises(IOError):
        style.setPageStyle(page, INVALID_STYLE_DIR)


def test_self_default(test_wikiroot: WikiDocument):
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]

    style.setPageStyle(page, style.getPageStyle(page))

    assert os.path.abspath(style.getPageStyle(page)) == os.path.abspath(
        style.getDefaultStyle()
    )


def test_self_special(test_wikiroot: WikiDocument):
    """
    Setting the current page style again must not change the page style.
    """
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]

    style.setPageStyle(page, EXAMPLE_STYLE_DIR)
    style.setPageStyle(page, style.getPageStyle(page))


def test_invalid_style_1(application: Application, test_wikiroot: WikiDocument):
    """
    An unknown key in a style template must not break HTML generation.
    """
    style = Style()
    page = test_wikiroot[WIKI_PAGE_TITLE]

    fname = os.path.join(page.path, style._styleFname)
    with open(fname, "w") as fp:
        fp.write(
            """<html>
<head>
</head>

<body>
<p>$content</p>

$invalidkey
</body>
</html>
"""
        )

    generator = HtmlGenerator(page, application)
    generator.makeHtml(Style().getPageStyle(page))

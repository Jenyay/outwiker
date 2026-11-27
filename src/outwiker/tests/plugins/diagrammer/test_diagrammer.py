
"""Tests for the (:diagram:) wiki command of the Diagrammer plugin."""

from pathlib import Path

import pytest

from outwiker.api.core.tree import WikiPage
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.thumbnails import Thumbnails
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory


@pytest.fixture
def test_page(wikiroot) -> WikiPage:
    """Wiki page the diagrams are parsed for."""
    return WikiPageFactory().create(wikiroot, "Страница 1", [])


@pytest.fixture
def parser(
    test_page: WikiPage,
    application,
    diagrammer_loader: PluginsLoader,
) -> Parser:
    """Wiki parser with the commands added by the Diagrammer plugin."""
    factory = ParserFactory()
    return factory.make(test_page, application)


@pytest.fixture
def thumb_path(test_page: WikiPage) -> Path:
    """Directory for the rendered diagrams. It is not created in advance."""
    return Path(Thumbnails(test_page).getThumbPath(create=False))


@pytest.fixture
def all_shapes() -> list[str]:
    """Shapes that the plugin is able to draw."""
    return [
        "actor",
        "beginpoint",
        "box",
        "circle",
        "cloud",
        "diamond",
        "dots",
        "ellipse",
        "endpoint",
        "mail",
        "minidiamond",
        "none",
        "note",
        "roundedbox",
        "square",
        "textbox",
        "flowchart.database",
        "flowchart.input",
        "flowchart.loopin",
        "flowchart.loopout",
        "flowchart.terminator",
    ]


def _get_image_prefix() -> str:
    """Beginning of the <img> tag with the rendered diagram."""
    return f'<img src="{Thumbnails.getRelativeThumbDir()}/__diagram_'


def _assert_rendered(parser: Parser, thumb_path: Path, text: str, count: int):
    """Check that the text is rendered to `count` diagrams without errors."""
    result = parser.toHtml(text)

    assert _get_image_prefix() in result

    # The parsing error message is wrapped in the <b> tag
    assert "<b>" not in result

    assert thumb_path.exists()
    assert len(list(thumb_path.iterdir())) == count


@pytest.mark.parametrize(
    "text, count",
    [
        pytest.param("(:diagram:)(:diagramend:)", 1, id="empty"),
        pytest.param("(:diagram:)Абырвалг -> Блаблабла(:diagramend:)", 1, id="single"),
        pytest.param(
            "(:diagram:)Абырвалг -> Блаблабла(:diagramend:)\n"
            "(:diagram:)Абыр -> валг -> Блаблабла(:diagramend:)",
            2,
            id="different",
        ),
        pytest.param(
            "(:diagram:)Абырвалг -> Блаблабла(:diagramend:)\n"
            "(:diagram:)Абырвалг -> Блаблабла(:diagramend:)",
            1,
            id="same",
        ),
    ],
)
def test_rendered(parser, thumb_path, text, count):
    _assert_rendered(parser, thumb_path, text, count)


def test_error(parser, thumb_path):
    text = "(:diagram:)a - b(:diagramend:)"

    result = parser.toHtml(text)

    assert _get_image_prefix() not in result

    # The parsing error message is wrapped in the <b> tag
    assert "<b>" in result

    # The directory for the thumbnails is created anyway
    assert thumb_path.exists()


def test_all_shapes(parser, all_shapes):
    template = "a{n}[shape = {shape}]"
    lines = ["(:diagram:)"]

    for number, shape in enumerate(all_shapes):
        lines.append(template.format(n=number, shape=shape))

    lines.append("(:diagramend:)")

    result = parser.toHtml("\n".join(lines))

    assert _get_image_prefix() in result

    # The parsing error message is wrapped in the <b> tag
    assert "<b>" not in result


def test_shapes_list(diagrammer_loader: PluginsLoader, all_shapes):
    from diagrammer.diagramrender import DiagramRender

    assert DiagramRender.shapes == sorted(all_shapes)

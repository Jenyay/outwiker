# -*- coding: utf-8 -*-

"""Tests for downloading web pages by the WebPage plugin."""

import urllib.request
from pathlib import Path

import pytest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.utilites.textfile import readTextFile

# Name of the directory where the downloaded files are stored
STATIC_DIR_NAME = "__download"

IMG_TEMPLATE = '<img src="{path}"'
CSS_TEMPLATE = '<link href="{path}"'
SCRIPT_TEMPLATE = '<script src="{path}"'
HREF_TEMPLATE = 'href="{path}"'
CSS_URL_TEMPLATE = 'url("{path}")'

# Directory with the test data of the WebPage plugin
_TESTDATA_PATH = Path("testdata/webpage")


def _path2url(path: Path) -> str:
    return "file:" + urllib.request.pathname2url(str(path.resolve()))


def _assert_referenced(
    content: str,
    template: str,
    *file_names: str,
    static_dir: bool = True,
) -> None:
    """Check that the downloaded content refers to the given files.

    References are built relative to the static directory unless
    the content is the downloaded file itself (``static_dir=False``).
    """
    for file_name in file_names:
        path = f"{STATIC_DIR_NAME}/{file_name}" if static_dir else file_name
        reference = template.format(path=path)
        assert reference in content, f"Reference not found: {reference}"


def _assert_not_referenced(content: str, template: str, *file_names: str) -> None:
    """Check that the downloaded content does not refer to the given files."""
    for file_name in file_names:
        reference = template.format(path=f"{STATIC_DIR_NAME}/{file_name}")
        assert reference not in content, f"Unexpected reference found: {reference}"


def _assert_downloaded(download_dir: Path, *file_names: str) -> None:
    """Check that the given files were downloaded into the directory."""
    assert download_dir.exists()

    for file_name in file_names:
        fname = download_dir / file_name
        assert fname.exists(), f"File was not downloaded: {fname}"


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Temporary directory with a non-ASCII name for the downloaded files."""
    path = tmp_path / "Абырвалг абыр"
    path.mkdir()
    return path


@pytest.fixture
def download_dir(temp_dir: Path) -> Path:
    """Directory where the static files are downloaded."""
    return temp_dir / STATIC_DIR_NAME


@pytest.fixture
def controller(temp_dir: Path, webpage_loader: PluginsLoader):
    from webpage.downloader import DownloadController

    return DownloadController(str(temp_dir), STATIC_DIR_NAME)


@pytest.fixture
def download_page(controller):
    """Factory fixture that downloads an HTML file from the test data."""
    from webpage.downloader import Downloader

    def _download(*relative_path: str):
        html_path = _TESTDATA_PATH.joinpath(*relative_path)
        downloader = Downloader()
        downloader.start(_path2url(html_path), controller)
        return downloader

    return _download


def test_content_img_example1(download_page):
    content = download_page("example1", "example1.html").contentResult

    _assert_referenced(
        content,
        IMG_TEMPLATE,
        "image_01.png",
        "картинка.png",
        "image_01_1.png",
        "image_02.png",
        "image_03.png",
    )
    _assert_not_referenced(content, IMG_TEMPLATE, "image_02_1.png", "image_03_1.png")


def test_content_css_example1(download_page):
    content = download_page("example1", "example1.html").contentResult

    _assert_referenced(
        content,
        CSS_TEMPLATE,
        "fname1.css",
        "fname2.css",
        "fname3.css",
        "fname4.css",
        "fname1_1.css",
    )
    _assert_not_referenced(content, CSS_TEMPLATE, "fname2_1.css")


def test_content_script_example1(download_page):
    content = download_page("example1", "example1.html").contentResult

    _assert_referenced(
        content,
        SCRIPT_TEMPLATE,
        "fname1.js",
        "fname2.js",
        "fname2_1.js",
        "fname3.js",
        "fname4.js",
    )
    _assert_not_referenced(content, SCRIPT_TEMPLATE, "fname1_1.js")


def test_title_example1(download_page):
    downloader = download_page("example1", "example1.html")

    assert downloader.success
    assert downloader.pageTitle == "Заголовок страницы"


def test_no_title(download_page):
    downloader = download_page("example_no_title", "example_no_title.html")

    assert downloader.success
    assert downloader.pageTitle is None


def test_content_example2(download_page):
    content = download_page("example2", "example2.html").contentResult

    _assert_referenced(
        content,
        IMG_TEMPLATE,
        "image_01.png",
        "image_01_1.png",
        "image_02.png",
    )
    _assert_not_referenced(content, IMG_TEMPLATE, "image_02_1.png")


def test_downloading_img_01(download_page, download_dir):
    download_page("example1", "example1.html")

    _assert_downloaded(
        download_dir,
        "image_01.png",
        "image_02.png",
        "image_03.png",
        "image_01_1.png",
    )


def test_downloading_img_02(download_page, download_dir):
    download_page("example2", "example2.html")

    _assert_downloaded(
        download_dir,
        "image_01.png",
        "image_02.png",
        "image_03.png",
    )


def test_downloading_img_03(download_page, download_dir):
    download_page("Пример 3", "пример 3.html")

    _assert_downloaded(
        download_dir,
        "image_01.png",
        "image_02.png",
        "image_03.png",
        "image_01_1.png",
    )


def test_downloading_img_urlquote(download_page, download_dir):
    downloader = download_page("example_urlquote", "example_urlquote.html")

    _assert_downloaded(download_dir, "рисунок.png")
    _assert_referenced(downloader.contentResult, IMG_TEMPLATE, "рисунок.png")


def test_downloading_favicon_01(download_page, download_dir, controller):
    downloader = download_page("example_favicon_01", "example.html")

    _assert_downloaded(download_dir, "favicon_1.png", "favicon_2.png")
    _assert_referenced(
        downloader.contentResult,
        HREF_TEMPLATE,
        "favicon_1.png",
        "favicon_2.png",
    )
    assert Path(controller.favicon) == download_dir / "favicon_1.png"


def test_downloading_favicon_02(download_page, download_dir, controller):
    download_page("example_favicon_02", "example.html")

    assert Path(controller.favicon) == download_dir / "favicon.png"
    _assert_downloaded(download_dir, "favicon.png")


def test_downloading_favicon_03(download_page, download_dir, controller):
    download_page("example_favicon_03", "example.html")

    assert Path(controller.favicon) == download_dir / "favicon.ico"
    _assert_downloaded(download_dir, "favicon.ico")


def test_downloading_css_rename(download_page, download_dir):
    downloader = download_page("example_css_rename", "example.html")

    _assert_downloaded(download_dir, "style.php.css")
    _assert_referenced(downloader.contentResult, HREF_TEMPLATE, "style.php.css")


def test_downloading_img_srcset_files(download_page, download_dir):
    download_page("example3", "example3.html")

    _assert_downloaded(
        download_dir,
        "image_01.png",
        "image_02.png",
        "image_03.png",
        "image_04.png",
    )


def test_downloading_img_srcset_content(download_page):
    downloader = download_page("example3", "example3.html")

    sample = (
        'srcset="{path}/image_02.png 2x, '
        '{path}/image_03.png w600, '
        '{path}/image_04.png"'
    ).format(path=STATIC_DIR_NAME)

    assert sample in downloader.contentResult


def test_downloading_css_01(download_page, download_dir):
    download_page("example1", "example1.html")

    _assert_downloaded(
        download_dir,
        "fname1.css",
        "fname2.css",
        "fname3.css",
        "fname4.css",
        "fname1_1.css",
    )


def test_downloading_css_import_01(download_page, download_dir):
    download_page("example1", "example1.html")

    _assert_downloaded(
        download_dir,
        "import1.css",
        "import2.css",
        "import3.css",
        "import4.css",
        "basic2.css",
        "basic3.css",
        "basic4.css",
        "basic5.css",
        "basic5_1.css",
        "basic6.css",
    )


def test_downloading_css_back_img_01(download_page, download_dir):
    download_page("example1", "example1.html")

    _assert_downloaded(
        download_dir,
        "back_img_01.png",
        "back_img_02.png",
        "back_img_03.png",
        "back_img_04.png",
        "back_img_05.png",
        "back_img_06.png",
    )


def test_downloading_css_url_01(download_page, download_dir):
    download_page("example1", "example1.html")

    content = readTextFile(download_dir / "fname1.css")

    _assert_referenced(
        content,
        CSS_URL_TEMPLATE,
        "import1.css",
        "back_img_01.png",
        "back_img_02.png",
        "back_img_03.png",
        "back_img_04.png",
        "back_img_05.png",
        "back_img_06.png",
        static_dir=False,
    )


def test_downloading_css_url_02(download_page, download_dir):
    download_page("example1", "example1.html")

    content = readTextFile(download_dir / "fname2.css")

    _assert_referenced(
        content,
        CSS_URL_TEMPLATE,
        "basic2.css",
        "basic4.css",
        "basic5.css",
        "basic6.css",
        static_dir=False,
    )

    # @import "basic3.css" is not a url() reference, so it is left as is
    assert "basic3.css" in content


def test_downloading_css_03(download_page, download_dir):
    download_page("Пример 3", "пример 3.html")

    _assert_downloaded(
        download_dir,
        "fname1.css",
        "fname2.css",
        "fname3.css",
        "fname4.css",
        "fname1_1.css",
    )


def test_downloading_javascript_01(download_page, download_dir):
    download_page("example1", "example1.html")

    _assert_downloaded(
        download_dir,
        "fname1.js",
        "fname2.js",
        "fname3.js",
        "fname4.js",
    )

#!/usr/bin/python
# -*- coding: utf-8 -*-

import builtins
import os
import os.path
import shutil
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Tuple, Callable, TextIO
from pathlib import Path

from invoke import task

from outwiker.build.utilites import getPython, print_info
from outwiker.build.defines import COVERAGE_PARAMS
from outwiker.build.builders import (
    BuilderWindows,
    BuilderPlugins,
    BuilderSnap,
)
from outwiker.build.versionstools import (
    display_version,
    InitUpdater,
    VersionsXmlUpdater,
    AppDataXmlUpdater,
)


@task
def plugins(c):
    """
    Create an archive with plugins (7z required)
    """
    builder = BuilderPlugins(c)
    builder.build()


@task
def win(c, is_stable=False, skiparchives=False, skipinstaller=False):
    """
    Build OutWiker for Windows
    """
    builder = BuilderWindows(
        c,
        is_stable=is_stable,
        create_archives=not skiparchives,
        create_installer=not skipinstaller,
    )
    builder.build()


@task
def run(c, args=""):
    """
    Run OutWiker from sources
    """
    c.run("{} -m outwiker {}".format(getPython(), args))


@task(iterable=["params"])
def test(c, params):
    """
    Run the unit tests
    """
    if not params:
        params = ["src/outwiker/tests"]

    params_str = " ".join(params)
    c.run(f"coverage run runtests.py {params_str}")


@task
def create_tree(c, maxlevel, nsiblings, path):
    """
    Create wiki tree for the tests
    """
    from outwiker.core.tree import WikiDocument

    builtins._ = lambda x: x
    wikiroot = WikiDocument.create(path)
    _create_tree(1, int(maxlevel), int(nsiblings), wikiroot)


def _create_tree(level, maxlevel, nsiblings, parent):
    from outwiker.pages.wiki.wikipage import WikiPageFactory

    if level <= maxlevel:
        for n in range(nsiblings):
            pagename = "page_{:03g}_{:03g}".format(level, n)
            print("Create page {}".format(pagename))

            newpage = WikiPageFactory().create(parent, pagename, [])
            newpage.content = "Абырвалг"
            newpage.icon = "images/outwiker_16.png"
            _create_tree(level + 1, maxlevel, nsiblings, newpage)


@task
def doc(c):
    """
    Build documentation
    """
    doc_path = "doc/_build"
    if os.path.exists(doc_path):
        shutil.rmtree(doc_path)

    with c.cd("doc"):
        c.run("make html")


@task
def coverage(c):
    """
    Create test coverage statistics
    """
    c.run("coverage report {} -i".format(COVERAGE_PARAMS))
    c.run("coverage html {} -i".format(COVERAGE_PARAMS))


@task(iterable=["params"])
def snap(c, params):
    """
    Build clean snap package
    """
    builder = BuilderSnap(c, params)
    builder.build()


@task
def set_version(c, version_str=""):
    """Set new OutWiker version for all files with versions"""
    if not version_str.strip():
        display_version()
        version_str = input(
            'Enter new OutWiker version in the format: "x.x.x.xxx [status]": '
        )

    version, status = _parse_version(version_str)
    for fname, updater in _get_version_updaters():
        _update_version_for_file(fname, updater.set_version, version, status)


@task
def add_new_version(c, version_str=""):
    """Append new version information to all files with versions"""
    if not version_str.strip():
        display_version()
        version_str = input(
            'Enter new OutWiker version in the format: "x.x.x.xxx [status]": '
        )

    version, status = _parse_version(version_str)
    for fname, updater in _get_version_updaters():
        _update_version_for_file(fname, updater.add_version, version, status)


@task
def set_release_date(c, date=""):
    """Set release date for current version"""
    if not date.strip():
        display_version()
        today = datetime.now().strftime("%Y-%m-%d")
        date = input(
            f"Enter OutWiker and plugins release date in the format: YYYY-MM-DD "
            f"(default: {today}): "
        ).strip()
        if not date:
            date = today

    for fname, updater in _get_version_updaters():
        print_info(f"Update file: {fname}")
        _set_release_date_for_file(fname, updater, date)

    _set_release_date_for_plugins(date)


def _get_version_updaters():
    return [
        (Path("src", "outwiker", "__init__.py"), InitUpdater()),
        (Path("need_for_build", "versions.xml"), VersionsXmlUpdater()),
        (
            Path("need_for_build", "linux", "net.jenyay.Outwiker.appdata.xml"),
            AppDataXmlUpdater(),
        ),
    ]


def _set_release_date_for_plugins(date_str: str):
    """
    Set release date for the first <version> tag in all versions.xml files.
    Only adds the date attribute if it's not already present.
    """
    # List of versions.xml files to process
    versions_xml_files = []

    # Add all versions.xml files from plugins
    plugins_dir = Path("plugins")
    for versions_file in plugins_dir.glob("*/versions.xml"):
        versions_xml_files.append(versions_file)

    for versions_file in versions_xml_files:
        _set_release_date_for_version_xml_file(versions_file, date_str)


def _set_release_date_for_version_xml_file(path: Path, date_str: str):
    """
    Set release date for the first <version> tag in a versions.xml file.
    Only adds the date attribute if it's not already present.
    """
    tree = ET.parse(str(path))
    root = tree.getroot()
    version_tag = root.find("version")

    if version_tag is None:
        return

    if "date" in version_tag.attrib:
        # Date attribute already exists, skip
        return

    version_tag.set("date", date_str)

    print_info(f"Update file: {path}")
    with open(path, "wb") as fp_out:
        fp_out.write(ET.tostring(root, encoding="UTF-8", xml_declaration=True))


def _parse_version(version_str: str) -> Tuple[List[int], str]:
    regexp = re.compile(r"(?P<numbers>(\d+)(\.\d+)*)(?P<status>\s+.*)?")
    match = regexp.match(version_str)
    numbers = [int(number) for number in match.group("numbers").split(".")]
    status = match.group("status")
    if status is None:
        status = ""
    return (numbers, status.strip())


def _update_version_for_file(
    path: str,
    updater_func: Callable[[TextIO, List[int], str], str],
    version: List[int],
    status: str,
):
    with open(path, encoding="utf-8") as fp_in:
        content_new = updater_func(fp_in, version, status)

    with open(path, "w", encoding="utf-8") as fp_out:
        fp_out.write(content_new)


def _set_release_date_for_file(path: str, updater, date_str: str):
    with open(path) as fp_in:
        content_new = updater.set_release_date(fp_in, date_str)

    with open(path, "w") as fp_out:
        fp_out.write(content_new)

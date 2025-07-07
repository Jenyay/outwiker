# -*- coding: utf-8 -*-

# List of the supported plugins
PLUGINS_LIST = [
    "autorenamer",
    "counter",
    "datagraph",
    "diagrammer",
    "export2html",
    "externaltools",
    "hackpage",
    "htmlformatter",
    "htmlheads",
    "lightbox",
    "livejournal",
    "markdown",
    "pagetypecolor",
    "readingmode",
    "recenteditedpages",
    "sessions",
    "snippets",
    "source",
    "spoiler",
    "statistics",
    "tableofcontents",
    "texequation",
    "thumbgallery",
    "webpage",
]

LANGUAGES = ["en", "de", "ru", "sv", "uk"]

BUILD_DIR = "build"
BUILD_LIB_DIR = "libs"
LINUX_BUILD_DIR = "linux"
WINDOWS_BUILD_DIR = "windows"
WINDOWS_EXECUTABLE_DIR = "outwiker_exe"
WINDOWS_INSTALLER_FILENAME = "outwiker_win_unstable.exe"
APPIMAGE_BUILD_DIR = "linux"
SNAP_BUILD_DIR = "linux"

SOURCES_DIR = "sources"
PLUGINS_DIR = "plugins"
PLUGIN_VERSIONS_FILENAME = "versions.xml"
PLUGIN_INFO_FILENAME = "plugin.xml"
OUTWIKER_VERSIONS_FILENAME = "versions.xml"
NEED_FOR_BUILD_DIR = "need_for_build"
COVERAGE_PARAMS = "--rcfile=.coveragerc"

WXPYTHON_SRC_DIR = "depends/wxpython"
WXPYTHON_BUILD_DIR = "wxpython"

PPA_DEV_PATH = "ppa:outwiker-team/dev"
PPA_UNSTABLE_PATH = "ppa:outwiker-team/unstable"
PPA_STABLE_PATH = "ppa:outwiker-team/ppa"

# Timeout in seconds
DOWNLOAD_TIMEOUT = 15
